import time

from src.models.entities import Weibo
from src.models import session_scope

from . import run_on_executor


def create(data):
    content = data.get('content')
    user_id = data.get('user_id')
    with session_scope() as db_session:
        weibo = Weibo(content=content, user_id=user_id)
        db_session.add(weibo)
        db_session.commit()
        print('debug controller res:', weibo.content)
        return {
            'id': weibo.id,
            'content': weibo.content,
            'user_id': weibo.user_id,
            'create_time': weibo.create_time
        }


@run_on_executor()
def create2(data):
    content = data.get('content')
    user_id = data.get('user_id')
    with session_scope() as db_session:
        weibo = Weibo(content=content, user_id=user_id)
        db_session.add(weibo)
        db_session.commit()
        print('debug controller res:', weibo.content)
        time.sleep(10)

        return {
            'id': weibo.id,
            'content': weibo.content,
            'user_id': weibo.user_id,
            'create_time': weibo.create_time
        }
