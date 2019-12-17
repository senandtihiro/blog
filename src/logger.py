# coding: utf-8
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
处理日志相关配置
"""


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
        'info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'debug',
            'filename': './log/info.log',
            'maxBytes': 1024 * 1024 * 200,
            'backupCount': 5,
            'encoding': 'utf-8'
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s:%(lineno)d | %(message)s',
        },
        'debug': {
            'format': '%(asctime)s - %(levelname)s - %(name)s:%(lineno)d | %(message)s',
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'info'],
            'propagate': True
        },
    }
}
