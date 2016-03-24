#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from flask.ext.cache import Cache
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CsrfProtect

from app.factory import create_app
from app.helper import register_blueprints

# 初始化Flask
app = create_app(__name__)
# 缓存设置
cache = Cache(app, config={'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple')})
# 定义数据库标示符
db = SQLAlchemy(app)
# 定义权限模块
security = Security(app)
# 定义跨域保护模块
csrf = CsrfProtect(app)

# 自动注册所有蓝图
register_blueprints(app, __name__, __path__)

__all__ = ['app', 'db', 'cache', 'security', 'csrf']
# End
