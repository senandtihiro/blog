from sanic import Sanic
from sanic.response import json

from src.config.base_config import Config
from sanic.exceptions import SanicException
from sanic.log import logger

from src.logger import LOGGING_CONFIG
from src.exceptions import ApiException
from src.routes.weibo import weibo_bp
from src.routes.auth import auth_bp


app = Sanic(name='blog', log_config=LOGGING_CONFIG)
app.blueprint(weibo_bp)
app.blueprint(auth_bp)


# 公共参数列表
COMMON_PARAM_LIST = [
    {"name": "os_type", "type": "str", "desc": "系统类型", "reg": r"\w+", "required": False},
    {"name": "os_version", "type": "str", "desc": "系统版本", "reg": r"\w+", "required": False},
    {"name": "app_channel", "type": "str", "desc": "APP渠道", "reg": r"\w+", "required": False},
    {"name": "app_version", "type": "str", "desc": "APP版本", "reg": r"\w+", "required": False},
    {"name": "device_uuid", "type": "str", "desc": "设备唯一标识", "reg": r"\w+", "required": False}
]


@app.exception(SanicException)
def json_error(request, exception):
    if isinstance(exception, ApiException):
        logger.info(f'request {request} raise exception')
        return json(
            {
                'error_code': exception.code,
                'message': exception.message,
            }
        )
    else:
        logger.error(f'server error {exception}')
        return json(
            {
                'error_code': 'ERROR',
                'message': '服务器内部异常',
            }
        )


# 加载配置文件
def configure_app():
    app.secret_key = 'secret key'
    app.config.from_object(Config)


# 加载蓝图模块
def register_routes(_app):
    _app.blueprint(weibo_bp)
    _app.blueprint(auth_bp)
    return _app


def create_db():
    from src.models import entities, engine
    entities.BaseModel.metadata.create_all(engine)


if __name__ == '__main__':
    configure_app()
    create_db()
    app = register_routes(app)
    app.run(host='0.0.0.0', port=8000, debug=True)
