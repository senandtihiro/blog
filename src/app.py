from sanic import Sanic
import logging

from src.config.base_config import Config
# from sanic_cors import CORS
# from aoiklivereload import LiveReloader

# from crud import crud_bp, db, ShanghaiPersonInfo, LOGO
# from . import CONFIG
# from src import db
# How is Support hot reload in Sanic?
# Just do it !
# reloader = LiveReloader()
# reloader.start_watcher_thread()
# logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
# logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
# logging_format += "%(message)s"
#
# logging.basicConfig(
#     format=logging_format,
#     level=logging.DEBUG
# )
# log = logging.getLogger()

app = Sanic(__name__)

# but due to not support http `options` method in sanic core (https://github.com/channelcat/sanic/issues/251).
# So have to use third package extension for Sanic-Cors. Thank you @ashleysommer!

# CORS(app,
#      automatic_options=True)  # resolve pre-flight request problem (https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)


@app.middleware('response')
async def custom_banner(request, response):
    response.headers["content-type"] = "application/json"


# 加载配置文件
def configure_app():
    app.secret_key = 'secret key'
    app.config.from_object(Config)


# 加载蓝图模块
def register_routes(app):
    from src.routes.weibo import weibo as routes_weibo
    app.blueprint(routes_weibo)


def create_db():
    from src.models import entities, engine
    entities.BaseModel.metadata.create_all(engine)


if __name__ == '__main__':
    configure_app()
    create_db()
    register_routes(app)
    app.run(host='0.0.0.0', port=8000, debug=True)
