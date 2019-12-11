import time
from functools import wraps
from itsdangerous import URLSafeSerializer
from hmac import compare_digest

from sanic.response import json
from sanic.log import logger

from src.config.base_config import Config
from src import exceptions
from src.models.entities import User
from src import client_info_from_request_data, get_client_ident
from src.cache import redis_cache
from src.models import session_scope


TOKEN_NAME = 'token'
TOKENID_PREFIX = 'weibo_user_'


async def create_and_cache_token(user_id, password, client_info):
    token_lifetime = Config.TOKEN_LIFETIME
    token = create_token(user_id, password, client_info)
    await redis_cache.set("{0}{1}".format(TOKENID_PREFIX, user_id), token, timeout=token_lifetime)
    return token


def create_token(user_id, password, client_info):
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


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized, user_id = await check_request_for_authorization_status(request)
            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                kwargs['user_id'] = user_id
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator


async def check_request_for_authorization_status(request):
    token_name = request.app.config.get("TOKEN_NAME", TOKEN_NAME)
    token = request.headers.get(token_name)
    if token is None:
        raise exceptions.TokenNotFound()
    else:
        # 解析token
        client_info = client_info_from_request_data(request.json)
        user_id, user_pwd_hash, create_time, token_lifetime = await check_token_common(token, client_info)
        # 判断token中user是否有效
        with session_scope() as db_session:
            user = db_session.query(User).filter_by(id=user_id).first()
            if user is None:
                logger.debug("无效的用户: user_id:%s", user_id)
                raise exceptions.UserNotFound()
            if user.status != 1:
                logger.debug("账号已禁用: user_id:%s, status:%s", user_id, user.status)
                raise exceptions.UserStatusAbnormal()

        return True, user_id


async def check_token_common(token, client_info):
    """
    验证token合法性
    :param token: token
    """
    # 判断token字符串是否合法
    key = Config.SECRET_KEY
    try:
        token_serializer = URLSafeSerializer(key)
        user_id, password, user_ident, token_lifetime, create_time = token_serializer.loads(token)
    except Exception as e:
        logger.debug(f"非法的登录凭证: {token}, {e}")
        raise exceptions.TokenErr(message="非法的登录凭证")

    # 判断token环境是否改变
    identifier = get_client_ident(client_info)
    if not compare_digest(str(user_ident), str(identifier)):
        raise exceptions.TokenError(message="登录环境改变")

    # 判断token缓存是否有效
    cached_token = await redis_cache.get("{0}{1}".format(TOKENID_PREFIX, user_id))
    logger.info(f'debug student cached token:{cached_token}, input token:{token}')
    if cached_token:
        if not compare_digest(cached_token, token):  # token不同时，把cached_token解析出来比对哪里有变化，以便给出精准提示
            try:
                _user_id, _password, _user_ident, _token_lifetime, _create_time = token_serializer.loads(cached_token)
            except Exception:
                raise exceptions.TokenErr(message="登录凭证已失效")
            if user_id != _user_id or password != _password:
                raise exceptions.TokenError(message="登录凭证已失效2")
            if user_ident != _user_ident:
                raise exceptions.TokenChanged(message="登录环境改变")
            if int(create_time) < int(_create_time):
                raise exceptions.TokenExpired(message="登录凭证已过期")
    else:
        raise exceptions.TokenExpired(message="登录凭证已过期")

    # 刷新token时间
    if token_lifetime:
        await redis_cache.set("{0}{1}".format(TOKENID_PREFIX, user_id), token, timeout=token_lifetime)

    return user_id, password, create_time, token_lifetime
