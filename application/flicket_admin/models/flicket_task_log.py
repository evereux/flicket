#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from application import db
from application.flicket.models import Base


class FlicketTaskLog(Base):
    """
    Log of an executed Celery task.

    Rows are written by the Celery signal handlers in `application/celery_app.py`:
    `task_prerun` creates the row (`STARTED`), `task_postrun` records the final
    state, result and duration, and `task_failure` records the exception.

    The Admin Panel lists these logs on the "Task Logs" page
    (`/flicket_admin/task_logs/`), and the `delete_old_task_logs` task removes
    rows older than `FlicketConfig.task_log_retention_days`.

    :param str celery_id: the Celery task id.
    :param str task_name: the Celery task name.
    :param str status: `STARTED`, `SUCCESS` or `FAILURE`.
    :param str args: JSON serialised task args.
    :param str kwargs: JSON serialised task kwargs.
    :param str result: JSON serialised return value on `SUCCESS`.
    :param str error: the exception text on `FAILURE`.
    :param datetime started_at: when the task started.
    :param datetime finished_at: when the task finished.
    :param float duration_seconds: how long the task ran in seconds.
    :param str worker_id: the Celery worker node name.
    """
    __tablename__ = 'flicket_task_log'

    id = db.Column(db.Integer, primary_key=True)

    celery_id = db.Column(db.String(64), unique=True, index=True, nullable=True)
    task_name = db.Column(db.String(128), index=True, nullable=False)
    status = db.Column(db.String(16), index=True, default='STARTED')
    args = db.Column(db.Text, nullable=True)
    kwargs = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    error = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Float, nullable=True)
    worker_id = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return f"<FlicketTaskLog {self.task_name} {self.status}>"
