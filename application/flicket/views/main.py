#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import redirect, url_for, request, render_template
from flask_login import login_required

from application import app
from application.flicket.forms.search import SearchTicketForm
from application.flicket.models.flicket_models import (FlicketStatus,
                                                       FlicketDepartment,
                                                       FlicketTicket,
                                                       FlicketPost,
                                                       FlicketCategory)
from application.flicket.models.flicket_user import FlicketUser
from . import flicket_bp


# tickets main
@flicket_bp.route(app.config['FLICKET'] + 'tickets/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKET'] + 'tickets/<int:page>/', methods=['GET', 'POST'])
@login_required
def tickets(page=1):
    form = SearchTicketForm()

    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    if form.validate_on_submit():
        redirect_url = FlicketTicket.form_redirect(form, page, url='flicket_bp.tickets')

        return redirect(redirect_url)

    ticket_query, form = FlicketTicket.query_tickets(form, department=department, category=category, status=status,
                                                     user_id=user_id, content=content)
    number_results = ticket_query.count()

    ticket_query = ticket_query.paginate(page, app.config['posts_per_page'])

    return render_template('flicket_tickets.html',
                           title='Tickets',
                           form=form,
                           tickets=ticket_query,
                           page=page,
                           number_results=number_results,
                           status=status,
                           department=department,
                           category=category,
                           user_id=user_id,
                           base_url='flicket_bp.tickets'
                           )


@flicket_bp.route(app.config['FLICKET'] + 'my_tickets/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKET'] + 'my_tickets/<int:page>/', methods=['GET', 'POST'])
@login_required
def my_tickets(page=1):
    form = SearchTicketForm()

    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    if form.validate_on_submit():
        redirect_url = FlicketTicket.form_redirect(form, page, url='flicket_bp.my_tickets')

        return redirect(redirect_url)

    ticket_query, form = FlicketTicket.query_tickets(form, department=department, category=category, status=status,
                                                     user_id=user_id, content=content)

    ticket_query = FlicketTicket.my_tickets(ticket_query)
    number_results = ticket_query.count()

    ticket_query = ticket_query.paginate(page, app.config['posts_per_page'])

    return render_template('flicket_tickets.html',
                           title='My Tickets',
                           form=form,
                           tickets=ticket_query,
                           page=page,
                           number_results=number_results,
                           status=status,
                           department=department,
                           category=category,
                           user_id=user_id,
                           base_url='flicket_bp.my_tickets'
                           )
