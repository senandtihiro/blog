#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

from sanic.exceptions import SanicException

# error code
# role   x-xx-xxx  level - module - code
# level: 1 - 9
# module: 01: db; 02: auth; 03: user;
# code: 001 002 ...
# level为1的，都需要退出到登录页面

except_dict = {
    'DbError': {
        'code': 101003,
        'message': "数据库写入错误"
    },
    'TokenNotFound': {
        'code': 202001,
        'message': "TokenNotFound"
    },
    'TokenError': {
        'code': 202002,
        'message': "TokenError"
    },
    'TokenChanged': {
        'code': 202003,
        'message': "TokenChanged"
    },
    'TokenExpired': {
        'code': 202004,
        'message': "TokenExpired"
    },
    'LoginFailed': {
        'code': 203001,
        'message': "LoginFailed"
    },
    'NeedLogin': {
        'code': 203002,
        'message': "NeedLogin"
    },
    'NotAllowed': {
        'code': 303003,
        'message': "not allowed"
    },
    'UserNotFound': {
        'code': 303004,
        'message': "User Not Found"
    },
    'PasswordError': {
        'code': 303005,
        'message': "Password Error"
    },
    'UsernameExists': {
        'code': 303006,
        'message': "Username Exists"
    },
    'UserStatusAbnormal': {
        'code': 303007,
        'message': "User Status Abnormal"
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
