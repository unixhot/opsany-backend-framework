# -*- coding: utf-8 -*-
from blueapps.conf.log import get_logging_config_dict
from blueapps.conf.default_settings import *  # noqa

# 这里是默认的 INSTALLED_APPS，大部分情况下，不需要改动
# 如果你已经了解每个默认 APP 的作用，确实需要去掉某些 APP，请去掉下面的注释，然后修改
# INSTALLED_APPS = (
#     'bkoauth',
#     # 框架自定义命令
#     'blueapps.contrib.bk_commands',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.sites',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     # account app
#     'blueapps.account',
# )

# 请在这里加入你的自定义 APP
from config import UPLOAD_PATH

INSTALLED_APPS += (
    "index",
    "base",
)

# 自定义中间件
MIDDLEWARE += (
    'corsheaders.middleware.CorsMiddleware',
)

# 所有环境的日志级别可以在这里配置
# LOG_LEVEL = 'INFO'

# STATIC_VERSION_BEGIN
# 静态资源文件(js,css等）在APP上线更新后, 由于浏览器有缓存,
# 可能会造成没更新的情况. 所以在引用静态资源的地方，都把这个加上
# Django 模板中：<script src="/a.js?v={{ STATIC_VERSION }}"></script>
# mako 模板中：<script src="/a.js?v=${ STATIC_VERSION }"></script>
# 如果静态资源修改了以后，上线前改这个版本号即可
# STATIC_VERSION_END
STATIC_VERSION = '1.0'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# CELERY 开关，使用时请改为 True，否则请保持为False。启动方式为以下两行命令：
# worker: python manage.py celery worker -l info
# beat: python manage.py celery beat -l info
IS_USE_CELERY = False

# CELERY 并发数，默认为 2，可以通过环境变量或者 Procfile 设置
CELERYD_CONCURRENCY = os.getenv('BK_CELERYD_CONCURRENCY', 2)

# CELERY 配置，申明任务的文件路径，即包含有 @task 装饰器的函数文件
CELERY_IMPORTS = (
)

# load logging settings
LOGGING = get_logging_config_dict(locals())

# 初始化管理员列表，列表中的人员将拥有预发布环境和正式环境的管理员权限
# 注意：请在首次提测和上线前修改，之后的修改将不会生效
INIT_SUPERUSER = []

# 使用mako模板时，默认打开的过滤器：h(过滤html)
MAKO_DEFAULT_FILTERS = ['h']

# BKUI是否使用了history模式
IS_BKUI_HISTORY_MODE = False

# 是否需要对AJAX弹窗登录强行打开
IS_AJAX_PLAIN_MODE = False


UPLOAD_USER_FILE_PATH = os.path.join(os.path.join(UPLOAD_PATH, "uploads/"), APP_CODE) + "/user_file/"
USER_FILE_PATH = os.path.join("uploads", APP_CODE, "user_file")

PATH_LIST = [UPLOAD_USER_FILE_PATH]


for PATH in PATH_LIST:
    if not os.path.exists(PATH):
        os.makedirs(PATH)


"""
以下为框架代码 请勿修改
"""
# celery settings
if IS_USE_CELERY:
    INSTALLED_APPS = locals().get('INSTALLED_APPS', [])
    import djcelery

    INSTALLED_APPS += (
        'djcelery',
    )
    djcelery.setup_loader()
    CELERY_ENABLE_UTC = False
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# remove disabled apps
if locals().get('DISABLED_APPS'):
    INSTALLED_APPS = locals().get('INSTALLED_APPS', [])
    DISABLED_APPS = locals().get('DISABLED_APPS', [])

    INSTALLED_APPS = [_app for _app in INSTALLED_APPS
                      if _app not in DISABLED_APPS]

    _keys = ('AUTHENTICATION_BACKENDS',
             'DATABASE_ROUTERS',
             'FILE_UPLOAD_HANDLERS',
             'MIDDLEWARE',
             'PASSWORD_HASHERS',
             'TEMPLATE_LOADERS',
             'STATICFILES_FINDERS',
             'TEMPLATE_CONTEXT_PROCESSORS')

    import itertools

    for _app, _key in itertools.product(DISABLED_APPS, _keys):
        if locals().get(_key) is None:
            continue
        locals()[_key] = tuple([_item for _item in locals()[_key]
                                if not _item.startswith(_app + '.')])
