#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime
import decimal
import json

from flask import request
from flask_login import login_required

from application import app
from application.flicket.models.flicket_models import (FlicketCategory,
                                                       FlicketDepartment,
                                                       FlicketTicket,
                                                       FlicketPost,
                                                       FlicketStatus)
from application.flicket.models.user import User
from . import flicket_api_bp


def alchemy_encoder(obj):
    """
    JSON encoder function for SQLAlchemy special cases.
    Take from: http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    """
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


# json api to query users
@flicket_api_bp.route(app.config['FLICKET_API'] + 'users/', methods=['GET', 'POST'])
@login_required
def api_users():
    filter = request.args.get('filter')

    query = User.query

    if filter:
        query = query.filter(User.username.ilike('%{}%'.format(filter)))

    my_list = []
    for u in query:
        sub_dict = {
            'id': u.id,
            'username': u.username,
            'email_': u.email,
            'name': u.name
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump


# json api to display departments
@flicket_api_bp.route(app.config['FLICKET_API'] + 'department/', methods=['GET', 'POST'])
@login_required
def api_departments():
    departments = FlicketDepartment.query.all()

    my_list = []
    for d in departments:
        sub_dict = {
            'id': d.id,
            'department': d.department,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump


# json api to display categories
# todo: change int to string to prevent 404 form errors.
@flicket_api_bp.route(app.config['FLICKET_API'] + 'category/', methods=['GET', 'POST'])
@flicket_api_bp.route(app.config['FLICKET_API'] + 'category/<int:id>/', methods=['GET', 'POST'])
@login_required
def api_categories(id=None):
    categories = FlicketCategory.query

    if id:
        categories = categories.filter_by(department_id=id)

    my_list = []
    for c in categories:
        sub_dict = {
            'id': c.id,
            'category': c.category,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump


# json api to display tickets
@flicket_api_bp.route(app.config['FLICKET_API'] + 'tickets/<int:page>/', methods=['GET', 'POST'])
@login_required
def api_tickets(page=1):

    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

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

        f1 = FlicketTicket.title.ilike('%' + content + '%')
        f2 = FlicketTicket.content.ilike('%' + content + '%')
        f3 = FlicketTicket.posts.any(FlicketPost.content.ilike('%' + content + '%'))
        tickets = tickets.filter(f1 | f2 | f3)

    tickets = tickets.order_by(FlicketTicket.id.desc())

    tickets = tickets.paginate(page, app.config['posts_per_page'])

    my_list = []
    for t in tickets.items:

        assigned = '-'

        if t.assigned_id:
            assigned = t.assigned.username

        sub_dict = {
            'id': t.id,
            'number': t.id_zfill,
            'title': t.title,
            'submitted_by': t.user.username,
            'priority': t.ticket_priority.priority,
            'date': t.date_added.strftime('%d/%m/%Y'),
            'replies': t.replies,
            'department': t.category.department.department,
            'category': t.category.category,
            'status': t.current_status.status,
            'assigned': assigned,
        }
        my_list.append(sub_dict)

    json_dump = json.dumps(my_list)

    return json_dump
