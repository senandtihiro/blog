from hashlib import sha512
from src.cache import redis_cache


def client_info_from_request_data(request_data):
    client_info = '-'.join([str(request_data.get('app_channel')),
                            str(request_data.get('os_type')),
                            str(request_data.get('device_uuid'))])
    return client_info


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
