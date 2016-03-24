#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import flask.ext.admin as admin
import flask.ext.login as login
from flask import redirect, url_for
from flask.ext.security.utils import encrypt_password
from wtforms import PasswordField
from app import db
from app.admin import sqla
from app.admin.models import User, Role, BackupLog
from app.helper import redirect_back


class CustomAdminIndexView(admin.AdminIndexView):
    """
        后台功能定义
    """

    @admin.expose('/')
    @login.login_required
    def index(self):
        return super(CustomAdminIndexView, self).index()

    @admin.expose('/clear_cache')
    @login.login_required
    def clear_cache(self):
        from app import cache
        cache.clear()
        return redirect_back(u'缓存已经成功更新。')


class UserView(sqla.ModelView):
    """
        用户管理视图
    """
    column_list = ['email', 'roles', 'active', 'last_login_at']

    form_columns = ['roles', 'email', 'active']

    column_details_exclude_list = ('password',)

    column_details_list = ('email', 'roles', 'active', 'login_count', 'last_login_at', 'current_login_at',)

    column_labels = dict(email=u'账号', new_password=u'密码', roles=u'角色', last_login_at=u'上次登录时间',
                         current_login_at=u'最后登录时间', active=u'是否启用', login_count=u'登录次数')

    can_view_details = True

    def __init__(self, name=None, category=None):
        super(UserView, self).__init__(User, db.session, name=name, category=category)

    def scaffold_form(self):
        form_class = super(UserView, self).scaffold_form()
        form_class.new_password = PasswordField(u'新密码')
        return form_class

    def on_model_change(self, form, model):
        if len(model.new_password):
            model.password = encrypt_password(form.new_password.data)


class RoleView(sqla.ModelView):
    """
        角色管理视图
    """
    column_list = ('name', 'date_created',)
    column_labels = dict(name=u'名称', description=u'描述', date_created=u'创建时间')
    form_excluded_columns = ['date_created']

    def __init__(self, name=None, category=None):
        super(RoleView, self).__init__(Role, db.session, name=name, category=category)


class BackupLogView(sqla.ModelView):
    """
        数据库备份视图
    """
    can_create = False
    can_delete = False
    can_edit = False

    column_labels = dict(event=u'事件', level=u'级别', admin=u'用户', msg=u'内容', ip=u'IP', date_created=u'时间')

    def __init__(self, name=None, category=None):
        super(BackupLogView, self).__init__(BackupLog, db.session, name=name, category=category)


class CleanCacheMenuLink(admin.base.MenuLink):
    """
        清空缓存
    """

    def is_accessible(self):
        if not login.current_user.is_authenticated:
            return False
        if not login.current_user.has_role(u'Administrator'):
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))


class AuthenticatedMenuLink(admin.base.MenuLink):
    """退出链接"""

    def is_accessible(self):
        if not login.current_user.is_authenticated:
            return False
        if not login.current_user.has_role(u'Administrator'):
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.index'))
