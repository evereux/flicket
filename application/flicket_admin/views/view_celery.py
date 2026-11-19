#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import render_template
from flask_babel import gettext
from flask_login import login_required

from application import app
from application.celery_app import celery

from . import admin_bp
from .view_admin import admin_permission


# show celery status
@admin_bp.route(app.config['ADMINHOME'] + 'celery/', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def celery_status():
    inspect = celery.control.inspect(timeout=2.0)
    broker_ok = True
    try:
        pong = inspect.ping()
        active_tasks = inspect.active() or {}
    except Exception:
        broker_ok = False
        pong = None
        active_tasks = {}
    workers = sorted(pong.keys()) if pong else []
    active = sum(len(tasks or []) for tasks in active_tasks.values())
    return render_template('admin_celery.html',
                           title=gettext('Celery Status'),
                           broker_url=app.config['CELERY_BROKER_URL'],
                           broker_ok=broker_ok,
                           workers=workers,
                           active=active)
