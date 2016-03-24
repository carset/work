#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from flask.ext.admin.contrib import sqla
from flask import redirect, url_for
from flask.ext.login import current_user


class ModelView(sqla.ModelView):
    """
        ModelView基类，定义了权限部分
    """

    def is_accessible(self):
        if current_user.is_authenticated and current_user.has_role(u'Administrator'):
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.index'))

# End
