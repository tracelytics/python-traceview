# instrumentation loader -- checks oboe.config['inst_enabled'] and imports
# as requested.  used by middleware and djangoware.
import oboe

def _enabled(m):
    return oboe.config['inst_enabled'][m]

def load_inst_modules():
    if _enabled('httplib2'):
        from oboeware import inst_httplib2
    if _enabled('memcache'):
        from oboeware import inst_memcache
    if _enabled('pymongo'):
        from oboeware import inst_pymongo