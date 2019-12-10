#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

from sanic.exceptions import SanicException

# error code
# role   x-xx-xxx  level - module - code
# level: 1 - 9
# module: 01: auth; 02: customer; 03: security; 04: tag; 05: attention 06: 参数检验 07:file ;08:channel ;
# code: 001 002 ...
# level为1的，都需要退出到登录页面

except_dict = {
    'LoginFailed': {
        'code': 201001,
        'message': "LoginFailed"
    },
    'NeedLogin': {
        'code': 101002,
        'message': "NeedLogin"
    },
    'DbError': {
        'code': 101003,
        'message': "数据库写入错误"
    },
    'NotAllowed': {
        'code': 201003,
        'message': "not allowed"
    },
    'UserNotFound': {
        'code': 201004,
        'message': "User Not Found"
    },
    'PasswordError': {
        'code': 201005,
        'message': "Password Error"
    },
    'UsernameExists': {
        'code': 201006,
        'message': "Username Exists"
    }
}


def __init__(self, **kwargs):
    ''' make returned error message'''
    # the replace for json format
    self.message = self.message.format(**kwargs)


def __str__(self):
    return self.message


def __repr__(self):
    return self.message


class ApiException(SanicException):
    def __init__(self, code, message=None, text=None, status_code=None):
        super().__init__(message)
        self.code = code
        self.message = message

        if status_code is not None:
            self.status_code = status_code



exceptions_list = []
bases = (ApiException,)
attrs = {
    '__init__': __init__,
    '__str__': __str__,
    '__repr__': __repr__
}

# generate error classes,
# add them to exception_list
# and then convert to exceptions tuple

for (eklass_name, attr) in except_dict.items():
    attrs.update(attr)
    eklass = type(str(eklass_name), bases, attrs)
    exceptions_list.append(eklass)
    globals().update({eklass_name: eklass})
