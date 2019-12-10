import time
import asyncio
import concurrent.futures
import time
from functools import partial, wraps

from itsdangerous import URLSafeSerializer
from hashlib import sha512

from src.config.base_config import Config
from src.cache import redis_cache


token_prefix = 'weibo_user_'


# 多线程异步的装饰器
def run_on_executor():
    "return：type asyncio.Future"

    # 参考文档：https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                # print(partial(fn, *args, **kwargs))
                return await loop.run_in_executor(pool, partial(fn, *args, **kwargs))
        return wrapper
    return decorator


async def create_and_cache_token(user_agent, user_id, password, client_info):
    token_lifetime = Config.TOKEN_LIFETIME
    token = create_token(user_agent, user_id, password, client_info)
    await redis_cache.set("{0}{1}".format(token_prefix, user_id), token, timeout=token_lifetime)
    return token


def create_token(user_agent, user_id, password, client_info):
    """
    生成token
    :param user_id:  缓存token的用户标识
    :param password: 用户密码
    :param client_info: 客户端信息
    :return: token
    """
    create_time = int(time.time())
    user_ident = get_client_ident(client_info)
    token_lifetime = Config.TOKEN_LIFETIME
    key = Config.SECRET_KEY
    token_serializer = URLSafeSerializer(key)
    token = token_serializer.dumps((user_id, password, user_ident, token_lifetime, create_time))

    return token


def get_client_ident(user_agent=None, var=None):
    """获取客户端标识"""
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    if var is None or var == "":
        base = str(user_agent)
    else:
        base = '{0}|{1}'.format(var, user_agent)
    h = sha512()
    h.update(base.encode('utf8'))
    return h.hexdigest()
