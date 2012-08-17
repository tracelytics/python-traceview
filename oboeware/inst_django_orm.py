""" Tracelytics instrumentation for Django ORM.

Copyright (C) 2011 by Tracelytics, Inc.
All rights reserved.
"""

import oboe
import re
import sys

def wrap_execute(func, f_args, f_kwargs, res):
    obj, sql = f_args[:2]
    kwargs = { 'Query' : sql }
    if 'NAME' in obj.db.settings_dict:
        kwargs['Database'] = obj.db.settings_dict['NAME']
    if 'HOST' in obj.db.settings_dict:
        kwargs['RemoteHost'] = obj.db.settings_dict['HOST']
    if 'ENGINE' in obj.db.settings_dict:
        if re.search('postgresql', obj.db.settings_dict['ENGINE']):
            kwargs['Flavor'] = 'postgresql'
    return kwargs

class CursorOboeWrapper(object):

    ###########################################################################
    # Django cursors can be wrapped arbitrarily deeply with the following API.
    # Each class contains a references to the DB object, and the next level
    # cursor. Control passes to the cursor in execute and executemany, wrapped
    # with whatever behavior the wrapper provides.
    ###########################################################################

    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else:
            return getattr(self.cursor, attr)

    def __iter__(self):
        return iter(self.cursor)

    def execute(self, sql, params=()):
        return self.cursor.execute(sql, params)

    def executemany(self, sql, param_list):
        return self.cursor.executemany(sql, param_list)


def wrap(module):
    try:
        cursor_method = module.BaseDatabaseWrapper.cursor
        if getattr(cursor_method, '_oboe_wrapped', False):
            return

        oboe_wrapper = oboe.log_method('djangoORM', callback=wrap_execute)
        setattr(CursorOboeWrapper, 'execute', oboe_wrapper(CursorOboeWrapper.execute))
        setattr(CursorOboeWrapper, 'executemany', oboe_wrapper(CursorOboeWrapper.executemany))

        def cursor_wrap(self):
            try:
                return CursorOboeWrapper(cursor_method(self), self)
            except Exception, e:
                print >> sys.stderr, "[oboe] Error in cursor_wrap", e
                raise
        cursor_wrap._oboe_wrapped = True

        setattr(module.BaseDatabaseWrapper, 'cursor', cursor_wrap)
    except Exception, e:
        print >> sys.stderr, "[oboe] Error in module_wrap", e
