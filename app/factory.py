#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import flask.ext.babelex as babel
from flask import Flask

from .helper import check_resource_dir, register_template_filter


def create_app(name=None, settings_override=None):
    # 初始化Flask
    flask = Flask(name or __name__)
    # 加载配置文件
    flask.config.from_object('config')
    # 加载自自定义配置
    if settings_override is not None:
        flask.config.from_object(settings_override)
    # 设置中文化
    babel.Babel(flask, default_locale='zh_hans_CN')
    # 检查应用临时目录
    check_resource_dir(flask.config.get('RESOURCE_DIR'))
    # 注册模板过滤器
    register_template_filter(flask)

    return flask


def create_celery_app(app, settings_override=None):
    """
        初始化异步任务框架
    :param app:
    :param settings_override:
    :return:
    """
    from flask.ext.celery import Celery
    celery = Celery(app.import_name, broker=app.config.get('CELERY_BROKER_URL'))
    celery.conf.update(app.config)
    celery.conf.update(settings_override)

    context_task = celery.Task

    class ContextTask(context_task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return context_task.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

# End
