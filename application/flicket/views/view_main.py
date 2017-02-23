#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import redirect, url_for, request, render_template
from flask_login import login_required

from application import app
from application.flicket.forms.search import SearchTicketForm
from application.flicket.models.flicket_models import (FlicketStatus,
                                                       FlicketDepartment,
                                                       FlicketTicket,
                                                       FlicketPost,
                                                       FlicketCategory)
from application.flicket.models.user import User
from . import flicket_bp


# tickets main
@flicket_bp.route(app.config['FLICKET'] + 'tickets_main/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKET'] + 'tickets_main/<int:page>/', methods=['GET', 'POST'])
@login_required
def tickets_main(page=1):

    form = SearchTicketForm()

    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    if form.validate_on_submit():

        department = ''
        category = ''
        status = ''

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user_id = user.id

        # convert form inputs to it's table title
        if form.department.data:
            department = FlicketDepartment.query.filter_by(id=form.department.data).first().department
        if form.category.data:
            category = FlicketCategory.query.filter_by(id=form.category.data).first().category
        if form.status.data:
            status = FlicketStatus.query.filter_by(id=form.status.data).first().status

        return redirect(url_for('flicket_bp.tickets_main',
                                content=form.content.data,
                                page=page,
                                department=department,
                                category=category,
                                status=status,
                                user_id=user_id,
                                ))

    # todo: get data from api
    # fixes url if first ends with and second starts with /
    # uri = generate_url(request.url_root, url_for('flicket_api_bp.api_tickets', page=1, department=department))
    # r = requests.get(uri)
    # json_response = r.text

    tickets = FlicketTicket.query
    if status:
        tickets = tickets.filter(FlicketTicket.current_status.has(FlicketStatus.status == status))
        form.status.data = FlicketStatus.query.filter_by(status=status).first().id
    if category:
        tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.category == category))
        form.category.data = FlicketCategory.query.filter_by(category=category).first().id
    if department:
        department_filter = FlicketDepartment.query.filter_by(department=department).first()
        tickets = tickets.filter(FlicketTicket.category.has(FlicketCategory.department == department_filter))
        form.department.data = department_filter.id
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

    tickets = tickets.paginate(page, app.config['posts_per_page'])

    return render_template('flicket_main.html',
                           title='Flicket - Tickets',
                           form=form,
                           tickets=tickets,
                           page=page,
                           number_results=number_results,
                           status=status,
                           department=department,
                           category=category,
                           user_id=user_id
                           )
