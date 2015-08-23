import sys
import libmc
import inspect
import msgpack
import functools
from cheap_flight.config import MEMCACHED_SERVERS


mc = libmc.Client(MEMCACHED_SERVERS)
IGNORED_MC_RETURNS = {
    libmc.MC_RETURN_OK,
    libmc.MC_RETURN_INVALID_KEY_ERR,
}
DEFAULT_EXPIRE_IN = 3600 * 24


class cache(object):
    def __init__(self, key_tmpl, expire_in=DEFAULT_EXPIRE_IN):
        self.key_tmpl = key_tmpl
        self.expire_in = expire_in

    def __call__(self, fn):

        @functools.wraps(fn)
        def _(*args, **kwargs):
            vv = inspect.getcallargs(fn, *args, **kwargs)
            key = self.key_tmpl.format(**vv)
            cached = mc.get(key)
            if cached is not None:
                return msgpack.loads(cached)
            rv = fn(*args, **kwargs)
            if rv is None:
                raise ValueError("return value is None")
            mc.set(key, msgpack.dumps(rv), self.expire_in)
            return rv
        return _


def main(argv):
    assert len(mc.version()) > 0  # make sure memcached is alive


if __name__ == '__main__':
    sys.exit(main(sys.argv))
