#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
Background tasks for Flicket.

Tasks run on Celery - see `application/celery_app.py` for the app and the
beat schedule.  Every execution is logged to the "Task Logs" admin page.
"""

import datetime
import time

from sqlalchemy import or_

from application import app, db
from application.celery_app import celery
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.email import FlicketMail
from application.flicket_admin.models.flicket_config import FlicketConfig
from application.flicket_admin.models.flicket_task_log import FlicketTaskLog


@celery.task
def email_outstanding_tickets():
    """
    Emails users of outstanding tickets: tickets created by or assigned to
    each user with `status_id != 2`. Email functionality has to be enabled.
    """
    with app.app_context():
        # find all users
        users = FlicketUser.query.all()
        for user in users:
            # that have created a ticket or have a ticket assigned to them.
            tickets = FlicketTicket.query.filter(or_(
                FlicketTicket.user == user,
                FlicketTicket.assigned == user,
            )).filter(
                FlicketTicket.status_id != 2)

            if tickets.count() > 0:
                mail = FlicketMail()
                mail.tickets_not_closed(user, tickets)
                time.sleep(10)


@celery.task
def delete_old_task_logs():
    """
    Deletes task log rows older than the configured retention period
    (`FlicketConfig.task_log_retention_days` days). A retention period of 0
    (or None) disables the cleanup.
    :return: the number of deleted rows.
    """
    with app.app_context():
        config = FlicketConfig.query.first()
        if config is None:
            return 0
        retention = config.task_log_retention_days
        if retention is None:
            # pre-existing config rows keep the default
            retention = 30
        if retention == 0:
            return 0
        cutoff = datetime.datetime.now() - datetime.timedelta(days=retention)
        deleted = FlicketTaskLog.query.filter(FlicketTaskLog.started_at < cutoff).delete(
            synchronize_session=False)
        db.session.commit()
        return deleted
