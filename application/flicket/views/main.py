#! usr/bin/python3
# -*- coding: utf8 -*-

import time

from flask import redirect, url_for, request, render_template
from flask_login import login_required

from application import app
from application.admin.models.user import User
from application.flicket.forms.flicket_forms import SearchTicketForm
from application.flicket.models.flicket_models import (FlicketStatus,
                                                       FlicketDepartment,
                                                       FlicketTicket,
                                                       FlicketPost,
                                                       FlicketCategory)
from . import flicket_bp


# tickets main
@flicket_bp.route(app.config['FLICKETHOME'] + 'tickets_main/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKETHOME'] + 'tickets_main/<int:page>/', methods=['GET', 'POST'])
@login_required
def tickets_main(page=1):
    start = time.time()

    form = SearchTicketForm()

    # These are used to generate the quick filter buttons in form.
    ticket_status = FlicketStatus.query.all()
    ticket_department = FlicketDepartment.query.all()
    ticket_category = FlicketCategory.query.all()

    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user_id = user.id

        return redirect(url_for('tickets_main',
                                content=form.content.data,
                                page=page,
                                category=category,
                                department=department,
                                user_id=user_id,
                                status=status,
                                ))

    tickets = FlicketTicket.query
    if status:
        tickets = tickets.filter(FlicketTicket.current_status.has(FlicketStatus.status == status))
    if category:
        tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.category == category))
    if department:
        department_filter = FlicketDepartment.query.filter_by(department=department).first()
        tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.department == department_filter))
    if user_id:
        tickets = tickets.filter_by(assigned_id=int(user_id))

    if content:
        # search the titles
        form.content.data = content

        f1 = FlicketTicket.title.ilike('%' + content + '%')
        f2 = FlicketTicket.content.ilike('%' + content + '%')
        f3 = FlicketTicket.posts.any(FlicketPost.content.ilike('%' + content + '%'))
        tickets = tickets.filter(f1 | f2 | f3)

    tickets = tickets.order_by(FlicketTicket.id.desc())
    number_results = tickets.count()

    tickets = tickets.paginate(page, app.config['POSTS_PER_PAGE'])

    duration = round(time.time() - start, 3)

    return render_template('flicket_main.html',
                           title='Flicket - Tickets',
                           form=form,
                           tickets=tickets,
                           page=page,
                           number_results=number_results,
                           status=status,
                           ticket_status=ticket_status,
                           department=department,
                           ticket_category=ticket_category,
                           ticket_department=ticket_department,
                           duration=duration
                           )
