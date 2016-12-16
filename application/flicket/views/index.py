#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime

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
    """ View showing flicket main page. We use this to display some stats."""
    s_closed = 'Closed'
    s_open = 'Open'
    s_wip = 'In Work'

    days = 7
    # converts days into datetime object
    days_obj = datetime.datetime.now() - datetime.timedelta(days=days)

    # initialise base query
    query = FlicketTicket.query
    total = FlicketTicket.query.count()
    in_work = query.filter(FlicketTicket.current_status.has(FlicketStatus.status == s_wip)).count()
    _open = query.filter(FlicketTicket.current_status.has(FlicketStatus.status == s_open)).count()
    total_days = query.filter(FlicketTicket.date_added > days_obj).count()

    # find how many tickets each department has.
    department_count = []
    departments = [i.id for i in FlicketDepartment.query.all()]
    for i in departments:
        department_filter = FlicketDepartment.query.filter_by(id=i).first()
        num = query.filter(FlicketTicket.category.has(FlicketCategory.department == department_filter)).count()
        department_count.append({department_filter.department, num})

    return render_template('flicket_index.html',
                           title='Flicket',
                           total=total,
                           in_work=in_work,
                           _open=_open,
                           total_days=total_days,
                           days=days,
                           department_count=department_count)
