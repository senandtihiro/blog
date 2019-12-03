from contextlib import contextmanager

from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, VARCHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sanic.log import logger
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker

from src.exceptions import InnerException


BaseModel = declarative_base()
MYSQL_URL = 'mysql+pymysql://root:111111@127.0.0.1:3306/blog?charset=utf8mb4'
# engine = create_engine(MYSQL_URL, echo=True)

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
                raise InnerException("ERR", "写入数据库错误")

    def delete(self):
        with session_scope() as db_session:
            db_session.delete(self)
            db_session.commit()

    # def to_dict(self, exclude_columns=None):
    #     if exclude_columns is None:
    #         exclude_columns = []
    #     d = {}
    #     for column in self.__table__.columns:
    #         if column.name in exclude_columns:
    #             continue
    #         d[column.name] = getattr(self, column.name)


class User(BaseModel, ModelMixin):
    __tablename__ = 't_user_info'
    name = Column(VARCHAR(32), nullable=False, comment='用户名')
    age = Column(Integer, default="", nullable=False, comment='用户年龄')


class Weibo(BaseModel, ModelMixin):
    __tablename__ = 't_weibo_info'

    content = Column(VARCHAR(512), nullable=False, comment='微博内容')
    user_id = Column(Integer, nullable=False, comment='用户ID')
