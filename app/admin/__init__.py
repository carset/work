#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# from .admin import admin
import flask.ext.admin as admin
from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.security.utils import encrypt_password
from app import db, security, app
from app.admin.views import CustomAdminIndexView, AuthenticatedMenuLink, UserView, RoleView, BackupLogView, \
    CleanCacheMenuLink
from .models import User, Role

admin = admin.Admin(app, name=u'管理后台', index_view=CustomAdminIndexView(name=u'首页'))

user_data_store = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, user_data_store)

admin.add_link(AuthenticatedMenuLink(name=u'退出', endpoint='security.logout'))

admin.add_view(UserView(category=u'系统信息', name=u'用户设置'))
admin.add_view(RoleView(category=u'系统信息', name=u'角色设置'))
admin.add_view(BackupLogView(category=u'系统信息', name=u'备份记录'))
admin.add_link(CleanCacheMenuLink(category=u'系统信息', name=u'更新缓存', endpoint='admin.clear_cache'))


@app.before_first_request
def auto_insert_super_user():
    """
        自动创建第一个管理员账户
    :return:
    """
    db.create_all()
    manager = user_data_store.find_or_create_role(name=u'Administrator', description=u'Administrator')
    user_data_store.find_or_create_role(name=u'Member', description=u'Member')
    user = user_data_store.find_user(email=u'admin')
    if user is None:
        user = user_data_store.create_user(email=u'admin', password=encrypt_password(u'admin'))
        db.session.commit()
        user_data_store.add_role_to_user(user, manager)
        db.session.commit()

# End
