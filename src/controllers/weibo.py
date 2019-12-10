import time

from src.models.entities import Weibo
from src.models import session_scope

from src.controllers import run_on_executor


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
def get_weibo_list(data):
    offset = data.get('offset', 0)
    limit = data.get('limit', 10)
    with session_scope() as db_session:
        weibo_list = db_session.query(Weibo).offset(offset).limit(limit)
        return [
            {
                'id': weibo.id,
                'content': weibo.content,
                'user_id': weibo.user_id,
                'create_time': weibo.create_time
            } for weibo in weibo_list
        ]


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
