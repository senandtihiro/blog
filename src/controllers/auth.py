from src import exceptions
from src.controllers import run_on_executor
from src.models import session_scope
from src.models.entities import User
from src.routes import create_and_cache_token
from .. import client_info_from_request_data


async def verify_user(request):
    """
    是否放到线程池中执行是可选的，所以不一定要加装饰器，这个时候只能优化sql，确保速度够快
    :param request:
    :return:
    """
    request_data = request.json
    username = request_data.get('username')
    password = request_data.get('password')

    # user_agent = request.headers.get('User-Agent')

    with session_scope() as db_session:
        user = db_session.query(User).filter_by(username=username).first()
        if not user:
            raise exceptions.UserNotFound()

        if not user.check_password(password):
            raise exceptions.PasswordError()

        client_info = client_info_from_request_data(request_data)
        token = await create_and_cache_token(user.id, password, client_info)

        return {
            'user_id': user.id,
            'token': token
        }


@run_on_executor()
def register_account(data):
    username = data.get('username')
    password = data.get('password')
    age = data.get('age')
    with session_scope() as db_session:
        user = User(username=username, password=password, age=age)
        db_session.add(user)
        db_session.commit()

        return {
            'username': user.username
        }
