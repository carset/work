#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from app.admin import admin

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# End
