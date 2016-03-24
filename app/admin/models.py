#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   admin.models
"""
from flask.ext.security import RoleMixin, UserMixin
from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class UserTrace(object):
    """
        用户登录追踪字段
    """
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(128))
    current_login_ip = db.Column(db.String(128))
    login_count = db.Column(db.Integer)


class Role(Base, RoleMixin):
    """
        Admin后台用户角色定义
    """
    __tablename__ = 'roles'

    name = db.Column(db.String(64))
    description = db.Column(db.String(128))

    def __unicode__(self):
        return u'%s' % self.name


class User(Base, UserMixin, UserTrace):
    """
        Admin后台用户定义
    """
    __tablename__ = 'users'

    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    roles = db.relationship(Role, secondary=roles_users, uselist=True)

    def __unicode__(self):
        return u'%s' % self.email


class BackupLog(Base):
    """
        数据备份表
    """
    __tablename__ = 'backup'

    event = db.Column(db.String(256))
    level = db.Column(db.String(128))
    admin = db.Column(db.String(128))
    msg = db.Column(db.Text())
    ip = db.Column(db.String(128))

    def __unicode__(self):
        return self.user_id

# create: 15/11/27
# End
