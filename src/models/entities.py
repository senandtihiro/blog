from contextlib import contextmanager
from hmac import compare_digest

from sanic.log import logger
from sqlalchemy import Column, Integer, VARCHAR, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from src import exceptions

BaseModel = declarative_base()
MYSQL_URL = 'mysql+pymysql://root:123456@45.63.60.244:3306/blog?charset=utf8mb4'
# MYSQL_URL = 'mysql+pymysql://root:111111@127.0.0.1:3306/blog?charset=utf8mb4'


engine = create_engine(MYSQL_URL,
                       pool_size=5,
                       max_overflow=5,
                       pool_recycle=3600,
                       poolclass=QueuePool)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(e)
        raise
    finally:
        session.close()


class ModelMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment="ID")
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        with session_scope() as db_session:
            print('debug db_session:', db_session)
            try:
                db_session.add(self)
                db_session.commit()
            except Exception as e:
                logger.error("将{}写入数据库错误: {}".format(self.__class__.__name__, e))
                raise exceptions.DbError("ERR", "写入数据库错误")

    def delete(self):
        with session_scope() as db_session:
            db_session.delete(self)
            db_session.commit()


class User(BaseModel, ModelMixin):
    __tablename__ = 't_user_info'
    username = Column(VARCHAR(32), nullable=False, comment='用户名')
    _password = Column(VARCHAR(256), nullable=False, comment='密码')
    age = Column(Integer, default="0", nullable=False, comment='用户年龄')
    status = Column(Integer, default="1", nullable=False, comment='用户状态')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_pwd):
        self._password = generate_password_hash(raw_pwd)

    def check_password(self, password, is_hash=False):
        if is_hash:
            return compare_digest(self.password, password)
        return check_password_hash(self.password, password)


class Weibo(BaseModel, ModelMixin):
    __tablename__ = 't_weibo_info'

    content = Column(VARCHAR(512), nullable=False, comment='微博内容')
    user_id = Column(Integer, nullable=False, comment='用户ID')
