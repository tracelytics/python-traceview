""" Tracelytics instrumentation for SQLAlchemy.

 Copyright (C) 2011 by Tracelytics, Inc.
 All rights reserved.
"""
import logging

import oboe


log = logging.getLogger('oboeware')


def main():
    dialect_wrappers = {
        'do_commit': do_commit,
        'do_rollback': do_rollback
    }

    module_class_mappings = (
        ('sqlalchemy.engine.default', 'DefaultDialect', {
            'do_commit': do_commit,
            'do_execute': do_execute,
            'do_executemany': do_execute,
            'do_rollback': do_rollback
        },),
        ('sqlalchemy.dialects.mysql.base', 'MySQLDialect', dialect_wrappers,),
        ('sqlalchemy.dialects.postgresql.base', 'PGDialect', dialect_wrappers,),
    )

    for mod, classname, mappings in module_class_mappings:
        try:
            cls = getattr(__import__(mod, fromlist=[classname]), classname)
        except AttributeError, ImportError:
            log.warn('Failed to import %s from %s for patch', cls, mod)
        else:
            wrap_methods(cls, mappings)


def wrap_methods(cls, mappings):
    for name, fn in mappings.items():
        try:
            base_method = getattr(cls, name)
        except AttributeError:
            log.warn('Failed to patch %s on %s', name, cls.__name__)
        else:
            oboe_fn = oboe.log_method(
                'sqlalchemy',
                store_backtrace=oboe._collect_backtraces('sqlalchemy'),
                callback=fn)(base_method)
            setattr(cls, name, oboe_fn)


def do_commit(_f, args, _kwargs, _ret):
    self, conn_fairy = args[:2]
    return base_info(self.name, conn_fairy.connection, 'COMMIT')


def do_execute(_f, args, _kwargs, _ret):
    self, cursor, stmt, params = args[:4]
    info = base_info(self.name, cursor.connection, stmt)
    if not oboe.config.get('sanitize_sql', False):
        info['QueryArgs'] = str(params)
    return info


def do_rollback(_f, args, _kwargs, _ret):
    self, conn_fairy = args[:2]
    return base_info(self.name, conn_fairy.connection, 'ROLLBACK')


def base_info(dialect_name, conn, query):
    return {
        'Flavor': dialect_name,
        'Query': query,
        'RemoteHost': remotehost_from_connection(dialect_name, conn)
    }


def remotehost_from_connection(flavor_name, conn):
    if flavor_name == 'mysql':
        return conn.get_host_info().split()[0].lower()

    if flavor_name == 'postgresql':
        host_part = [part for part in conn.dsn.split()
                     if part.startswith('host=')]
        if host_part:
            return host_part[0].split('=')[1]


main()
