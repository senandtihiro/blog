from sanic import Sanic
from sanic.response import json

from src.config.base_config import Config
from sanic.exceptions import SanicException


app = Sanic(__name__)


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
    return json(
        {
            'error_code': exception.code,
            'message': exception.message,
        }
    )


# 加载配置文件
def configure_app():
    app.secret_key = 'secret key'
    app.config.from_object(Config)


# 加载蓝图模块
def register_routes(app):
    from src.routes.weibo import weibo as routes_weibo
    from src.routes.auth import auth as routes_auth
    app.blueprint(routes_weibo)
    app.blueprint(routes_auth)


def create_db():
    from src.models import entities, engine
    entities.BaseModel.metadata.create_all(engine)


if __name__ == '__main__':
    configure_app()
    create_db()
    register_routes(app)
    app.run(host='0.0.0.0', port=8000, debug=True)