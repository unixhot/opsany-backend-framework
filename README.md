# OpsAny后端开发框架

OpsAny后端开发框架，提供给用户之间在OpsAny社区版上开发的能力，集成了OpsAny社区版的统一认证、统一权限、消息通知、动态注意、国际化等内容，实现开箱即用。

## 代码结构介绍

OpsAny后端开发框架，支持Python3，默认使用Python 3.6.8版本。

### 项目目录结构

```bash
.
|-- base                        # OpsAny 头部公共api(可选择在当前app下开发,或重新创建app)
|   |-- migrations               # 数据库初始化文件包含基础用户表
|   |-- utils                    # 存放该应用相关组件
|   |-- __init__.py
|   |-- admin.py
|   |-- base_views.py           # 基础头部相关接口，包括菜单、导航、消息和个人信息等
|   |-- constant.py.py           # 当前应用常量信息
|   |-- urls.py                 # 接口路由
|   |-- models.py               # 数据库表，内涵基础用户表
|   |-- tests.py                # 单元测试文件
|   |-- views.py                # 可以写Views
|-- blueapps                    # Python 开发框架模块
|-- blueking                    # ESB 调用模块
|-- component                   # 公共组件
|-- config                      # 应用配置目录
|   |-- __init__.py               # 应用 RUN_VER（ieod/clouds/qcloud）、APP_CODE 和 SECRET_KEY 等配置
|   |-- dev.py                    # 本地开发配置（开发团队共享）
|   |- default.py                # 全局配置
|   |- prod.py                   # 生产环境配置
|   |- stag.py                   # 预发布环境配置
|-- index                        # 平台入口
|   |-- __init__.py
|   |-- admin.py
|   |-- urls.py
|   |-- models.py
|   |-- tests.py
|   |-- views.py
|-- static                      # 公共静态文件
|   |-- css                        # 公共 css
|   |-- img                        # 公共 img
|   |-- js                        # 公共 js
|   |   |-- csrftoken.js            # CSRFTOKEN
|   |   |-- settings.js             # 异常处理
|   |-- logo.png                   # 平台图标
|-- templates                   # 公共模板文件
|   |-- admin                     # admin 模板文件
|   |   |-- base_site.html
|   |   |-- login.html
|   |-- base.html                 # Django 模板基础文件，其他的页面可以从这里继承
|   |-- index.html                # 平台前端入口
|-- app.yml                       # 生产打包部署使用
|-- framework.png                 # 平台LOGO,需要与项目名一致
|-- manage.py                   # Django 工程 manage
|-- requirements.txt            # 依赖的 python 包列表
|-- settings.py                 # Django 工程 settings
|-- urls.py                     # Django 工程主路由 URL 配置
|-- wsgi.py                     # WSGI 配置
|-- runtime.txt                 # Python 版本配置文件，默认指向 Python 3.6.8 版本
```

### 常用配置说明

- App 基本信息

在 config/_\_init__.py 可以查看 App 基本信息，请修改： APP_CODE 、SECRET_KEY （用于 App 认证）和 BK_URL 、BK_PAAS_URL (平台的URL)。RUN_VER 是当前 App 运行的 PaaS 版本，请不要修改。

- App 运行环境

在 config/dev.py、config/stag.py、config/prod.py 中都有一个 RUN_MODE 的变量，用来标记 App 运行环境（DEVELOP：本地环境，STAGING：预发布环境，PRODUCT：正式环境），请不要修改。

- 日志级别和路径

开发框架默认配置的日志级别是 INFO，你可以在 config/default.py 修改 LOG_LEVEL 变量，会对所有运行环境生效，你也可以单独修改 config/dev.py、config/stag.py、config/prod.py 文件，详情请参考本文“7. 日志使用”。
开发框架已经自动帮你配置了线上运行环境的日志路径；
本地的日志放在和项目根目录同一级的 logs 目录下，以 APP_CODE 命名的文件夹中，其中 {APP_CODE}-django.log 是应用日志，{APP_CODE}-celery.log 是 celery 日志，{APP_CODE}-component.log 是组件日志，{APP_CODE}-mysql.log 是数据库日志。

- 数据库配置

本地数据库配置请在 config/dev.py 修改 DATABASES 变量；多人合作开发建议在根目录下新建 local_settings.py 文件，并配置 DATABASES 变量，并且在版本控制中忽略 local_settings.py，这样的好处是防止多人合作开发时本地配置不一致导致代码冲突。
线上运行环境的数据库配置不用自己配置，不过你可以线上运行环境通过 django.settings.DATABASES 获取数据库配置。



## 开发环境准备

- [开发手册](./docs/deploy.md) 
