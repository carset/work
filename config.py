#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   应用配置文件
"""
import os

# 调试开关
DEBUG = True

SECRET_KEY = '!@#$^&*(#OIs8S7a&^>'

# 启用CSRF保护
WTF_CSRF_ENABLED = True

# 数据库配置信息
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/app_20160315?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 权限账户信息配置
SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
SECURITY_FORGOT_PASSWORD_TEMPLATE = 'security/forgot_password.html'
SECURITY_TRACKABLE = True  # 跟踪用户登录信息
SECURITY_RECOVERABLE = True  # 找回密码
SECURITY_CHANGEABLE = True  # 修改密码
SECURITY_REGISTERABLE = True  # 新用户注册

# 是否打印SQL语句到控制台
SQLALCHEMY_ECHO = False

# 是否重建数据库
REBUILD_DATABASE = False

# 重置管理员密码
RESET_ADMIN_PASSWORD = True

# 上传资源的存储目录
RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'tmp')

STATIC_URI = ''
SITE_URI = 'http://localhost'

# 异步Celery配置
CELERY_BROKER_URL = 'amqp:/'

CELERY_RESULT_BACKEND = 'amqp:/'


# End
