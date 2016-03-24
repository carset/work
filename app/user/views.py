#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import Blueprint

user_view = Blueprint('user_view', __name__, url_prefix='/')


@user_view.route('')
def default_page():
    return "OK"

# End
