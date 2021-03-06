import asyncio
import concurrent.futures
from functools import partial

from sanic import Blueprint
from sanic.response import json
from ..controllers import weibo as weibo_controller

from . import authorized

weibo_bp = Blueprint('weibo', url_prefix='/weibo')


"""
@api {post} /weibo/create 创建微博
@apiVersion 0.1.0
@apiDescription 管理员创建一个用户
@apiGroup Weibo

@apiParam {String} content      微博内容

@apiSuccess {Object} data 创建成功，返回该weibo
"""

@weibo_bp.route('/create', methods=['POST'])
@authorized()
async def create(request, **kwargs):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result = await loop.run_in_executor(
    #         pool, weibo_controller.create, request.json)
        user_id = kwargs.get('user_id')
        result = await loop.run_in_executor(pool, partial(weibo_controller.create, request.json, user_id))

        return json(result)


"""
@api {post} /weibo/get_weibo_list 获取所有的微博列表
@apiVersion 0.1.0
@apiDescription 获取所有的微博列表
@apiGroup Weibo

@apiParam {int} offset  <int>    <可选>    分页偏移量，默认0
@apiParam {int} limit   <int>    <可选>    每次获取条数，默认10

@apiSuccess {[]} data 创建成功，返回该weibo
"""

@weibo_bp.route('/get_weibo_list', methods=['POST'])
async def get_weibo_list(request):
    res = await weibo_controller.get_weibo_list(request.json)
    return json(res)


@weibo_bp.route('/create2', methods=['POST'])
async def create(request):
    res = await weibo_controller.create2(request.json)
    return json(res)


@weibo_bp.route('/')
async def index(request):
    return json({
        'hello': 'world'
    })
