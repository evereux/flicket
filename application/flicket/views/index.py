#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import time

from flask import render_template, g
from flask_login import login_required

from . import flicket_bp
from application import app
from application.flicket.models.flicket_models import (FlicketTicket,
                                                       FlicketStatus,
                                                       FlicketDepartment,
                                                       FlicketCategory)

# view users
@flicket_bp.route(app.config['FLICKET'], methods=['GET', 'POST'])
@login_required
def index():

    """ View showing flicket main page. We use this to display some statistics."""
    s_closed = 'Closed'
    s_open = 'Open'
    s_wip = 'In Work'

    days = 7
    # converts days into datetime object
    days_obj = datetime.datetime.now() - datetime.timedelta(days=days)

    # initialise base query
    query = FlicketTicket.query
    total = FlicketTicket.query.count()
    total_days = query.filter(FlicketTicket.date_added > days_obj).count()

    # get list of statuses
    statuses = [({'id': s.id, 'status': s.status}, {}) for s in FlicketStatus.query.order_by(FlicketStatus.status).all()]
    # find number of tickets for each status
    for s in statuses:
        ticket_num = query.filter(FlicketTicket.current_status.has(FlicketStatus.id == s[0]['id'])).count()
        s[1]['ticket_num'] = ticket_num

    # get list of departments
    departments = [({'id': d.id, 'department': d.department}, []) for d in FlicketDepartment.query.all()]

    # department_filter = FlicketDepartment.query.filter_by(department=department).first()
    # tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.department == department_filter))

    # find number of tickets for each department based on status
    for d in departments:
        for s in statuses:
            department_filter = query.filter(FlicketTicket.category.has(FlicketCategory.department_id == d[0]['id']))
            ticket_num = department_filter.filter(FlicketTicket.current_status.has(FlicketStatus.id == s[0]['id'])).count()
            d[1].append(({'status': s[0]['status']}, {'total_num': ticket_num}))

    return render_template('flicket_index.html',
                           title='Flicket',
                           total=total,
                           total_days=total_days,
                           days=days,
                           statuses=statuses,
                           departments=departments)
