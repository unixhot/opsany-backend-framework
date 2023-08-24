# -*- coding: utf-8 -*-

from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 本地开发环境
RUN_MODE = 'DEVELOP'

# APP本地静态资源目录
STATIC_URL = '/static/'
UPLOAD_PATH = "D:/opsany/"
UPLOAD_SCRIPT_PATH = os.path.join("uploads", APP_CODE, "script")
UPLOAD_COMMAND_PATH = os.path.join("uploads", APP_CODE, "command")

PATH_LIST = [
    os.path.join(UPLOAD_PATH, UPLOAD_SCRIPT_PATH),
    os.path.join(UPLOAD_PATH, UPLOAD_COMMAND_PATH)
]

for PATH in PATH_LIST:
    if not os.path.exists(PATH):
        os.makedirs(PATH)

# APP静态资源目录url
# REMOTE_STATIC_URL = '%sremote/' % STATIC_URL

# Celery 消息队列设置 RabbitMQ
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# Celery 消息队列设置 Redis
BROKER_URL = 'redis://localhost:6379/0'

DEBUG = True

# 本地开发数据库设置
# USE FOLLOWING SQL TO CREATE THE DATABASE NAMED APP_CODE
# SQL: CREATE DATABASE `framework_py` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; # noqa: E501
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': APP_CODE,
        'USER': "root",
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}


# 线上bk_token，本地调试使用
BK_TOKEN = "h3eQK4Li1SrZE61YnXUJBTHIockFarv5GO4JPBY30lM"
# SITE_URL本地调试指定为空
SITE_URL = {"SITE_URL": ""}


# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings.py 加入版本管理忽略文件中
try:
    from .local_settings import *  # noqa
except ImportError:
    pass

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)