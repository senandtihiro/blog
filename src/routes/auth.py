from sanic import Blueprint
from sanic.response import json

from src.controllers import auth as auth_controller

auth = Blueprint('auth', url_prefix='/auth')


"""
@api {post} /auth/login 登入
@apiVersion 0.1.0
@apiDescription 用户登入
@apiGroup Auth

@apiParam {String} username     用户名
@apiParam {String} password     密码

@apiSuccess {int} user_id     当前登入用户ID
@apiSuccess {str} token     当前登入用户token
"""


@auth.route("/login", methods=["POST"])
async def login(request):
    res = await auth_controller.verify_user(request)
    return json(res)


"""
@api {post} /auth/register 注册
@apiVersion 0.1.0
@apiDescription 用户注册
@apiGroup Auth

@apiParam {String} username     用户名
@apiParam {String} password     密码
@apiParam {int} age     年龄

@apiSuccess {string} username     当前注册用户名
"""


@auth.route("/register", methods=["POST"])
async def register_account(request):
    data = await auth_controller.register_account(request.json)

    return json({
        "code": 0,
        "data": data
    })
