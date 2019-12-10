# coding: utf-8
"""
缓存插件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import json
from src.config.base_config import Config


try:
    import aioredis
except ImportError:
    raise RuntimeError('Redis module not found')


def dump_object(value):
    return json.dumps(value)


def load_object(value):
    if value is None:
        return None
    try:
        return json.loads(value)
    except TypeError:
        return None


class RedisCache(object):
    """redis缓存"""
    def __init__(self, redis_uri='', key_prefix='', key_timeout=None, **kwargs):
        self.redis_uri = 'redis://localhost:6379/0'
        self._client = None
        self.key_prefix = ''
        self.key_timeout = -1

    async def connect(self, redis_uri='', key_prefix='', key_timeout=None, **kwargs):
        self.key_prefix = key_prefix if key_prefix else Config.REDIS_KEY_PREFIX
        self.key_timeout = key_timeout if key_timeout else Config.REDIS_KEY_TIMEOUT
        _client = await aioredis.create_redis_pool(self.redis_uri)
        return _client

    def _normalize_timeout(self, timeout):
        if timeout is None:
            timeout = self.key_timeout
        elif timeout == 0:
            timeout = -1
        return timeout

    def _key(self, key, key_prefix=True):
        if self.key_prefix and key_prefix:
            return self.key_prefix + key
        return key

    async def get(self, key, key_prefix=True):
        connection = await self.connect()
        return load_object(await connection.get(self._key(key, key_prefix)))

    async def set(self, key, value, timeout=None, key_prefix=True):
        connection = await self.connect()
        key = self._key(key, key_prefix)
        timeout = self._normalize_timeout(timeout)
        value = dump_object(value)
        if timeout == -1:
            result = await connection.set(key, value)
        else:
            result = await connection.setex(key, timeout, value)
        return result


redis_cache = RedisCache()
