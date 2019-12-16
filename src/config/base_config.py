import os


class Config():
    """
    公有配置
    Basic config for demo02
    """
    # Application config
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    MAX_PER_PAGE = 5

    SQLALCHEMY_POOL_SIZE = 100      # 连接池个数
    SQLALCHEMY_POOL_TIMEOUT = 30    # 超时时间，秒
    SQLALCHEMY_POOL_RECYCLE = 3600  # 空连接回收时间，秒
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/training?charset=utf8mb4"
    REDIS_KEY_PREFIX = 'blog_'
    REDIS_KEY_TIMEOUT = 3600
    TOKEN_LIFETIME = 7 * 24 * 60 * 60
    SECRET_KEY = 'hard to guess string'
