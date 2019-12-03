import time
import asyncio
import concurrent.futures

from functools import partial, wraps


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
