#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
Celery app for Flicket.

The app is created here and configured from the Flask app config.  Periodic
tasks (and other background work) live in `application/tasks.py`, and the
beat schedule for them is defined below.

Every task execution is logged to the `FlicketTaskLog` model by the Celery
signal handlers defined below - the Admin Panel shows these logs on the
"Task Logs" page (`/flicket_admin/task_logs/`).
"""

import datetime
import json

from celery import Celery
from celery import signals
from celery.schedules import crontab

from application import app, db
from application.flicket_admin.models.flicket_task_log import FlicketTaskLog


def create_celery(app):
    """
    Create the Celery app configured from the Flask app config.
    :param app: the Flask app.
    :return: the Celery app.
    """
    celery = Celery(app.name)
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config.get('CELERY_RESULT_BACKEND'),
        timezone=app.config.get('CELERY_TIMEZONE', 'UTC'),
        enable_utc=True,
        task_track_started=True,
    )
    celery.conf.beat_schedule = {
        'email-outstanding-tickets': {
            'task': 'application.tasks.email_outstanding_tickets',
            'schedule': crontab(hour=9, minute=0),
        },
        'delete-old-task-logs': {
            'task': 'application.tasks.delete_old_task_logs',
            'schedule': crontab(hour=3, minute=0),
        },
    }
    return celery


celery = create_celery(app)


def _now():
    return datetime.datetime.now()


def _store_json(value):
    """JSON dump of task args/kwargs/results; falls back to str()."""
    if value is None:
        return None
    try:
        return json.dumps(value, default=str)
    except (TypeError, ValueError):
        return str(value)


def _log_row(task_id):
    return FlicketTaskLog.query.filter_by(celery_id=task_id).first()


@signals.task_prerun.connect
def on_task_prerun(sender=None, task_id=None, task=None, args=None, kwargs=None, **extra):
    """Create the STARTED log row when a task starts running."""
    if task is None:
        return
    with app.app_context():
        row = FlicketTaskLog(
            celery_id=task_id,
            task_name=task.name,
            status='STARTED',
            args=_store_json(args),
            kwargs=_store_json(kwargs),
            worker_id=getattr(task.request, 'hostname', None),
            started_at=_now(),
        )
        db.session.add(row)
        db.session.commit()


@signals.task_postrun.connect
def on_task_postrun(sender=None, task_id=None, task=None, state=None, retval=None, **extra):
    """Record the final state, result and duration when a task finishes."""
    with app.app_context():
        row = _log_row(task_id)
        if row is None:
            return
        now = _now()
        row.status = state or 'SUCCESS'
        row.finished_at = now
        if row.started_at:
            row.duration_seconds = (now - row.started_at).total_seconds()
        if state == 'SUCCESS':
            row.result = _store_json(retval)
        db.session.commit()


@signals.task_failure.connect
def on_task_failure(sender=None, task_id=None, task=None, exception=None, einfo=None, **extra):
    """Record the failure and the exception when a task raises."""
    with app.app_context():
        row = _log_row(task_id)
        if row is None:
            return
        now = _now()
        row.status = 'FAILURE'
        error = exception or einfo
        row.error = str(error) if error is not None else None
        row.finished_at = now
        if row.started_at:
            row.duration_seconds = (now - row.started_at).total_seconds()
        db.session.commit()


# The tasks are imported last so they can bind to this app.
from application import tasks  # noqa: E402
