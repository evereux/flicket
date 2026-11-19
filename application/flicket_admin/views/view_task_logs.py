#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort
from flask import render_template
from flask import request
from flask_babel import gettext
from flask_login import login_required

from application import app
from application.flicket_admin.models.flicket_task_log import FlicketTaskLog

from . import admin_bp
from .view_admin import admin_permission


TASK_LOGS_PER_PAGE = 25


@admin_bp.route(app.config['ADMINHOME'] + 'task_logs/', methods=['GET'])
@admin_bp.route(app.config['ADMINHOME'] + 'task_logs/<int:page>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def task_logs(page=1):
    query = FlicketTaskLog.query.order_by(FlicketTaskLog.started_at.desc(), FlicketTaskLog.id.desc())

    status_filter = request.args.get('status', '')
    if status_filter in ('STARTED', 'SUCCESS', 'FAILURE'):
        query = query.filter(FlicketTaskLog.status == status_filter)

    logs = query.paginate(page=page, per_page=TASK_LOGS_PER_PAGE)
    return render_template('admin_task_logs.html',
                           title=gettext('Task Logs'),
                           logs=logs,
                           status_filter=status_filter)


@admin_bp.route(app.config['ADMINHOME'] + 'task_logs/<int:log_id>/detail/', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def task_log_detail(log_id):
    log = FlicketTaskLog.query.filter_by(id=log_id).first()
    if log is None:
        abort(404)
    return render_template('admin_task_log_detail.html',
                           title=gettext('Task Log Detail'),
                           log=log)
