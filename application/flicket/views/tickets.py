#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from datetime import datetime

from flask import redirect, request, make_response, render_template, Response, url_for
from flask_babel import gettext
from flask_login import login_required

from application import app
from application.flicket.forms.search import SearchTicketForm
from application.flicket.models.flicket_models import FlicketTicket
from . import flicket_bp


def clean_csv_data(input_text):
    output_text = input_text.replace('"', "'")

    return output_text


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
        redirect_url = FlicketTicket.form_redirect(form, url='flicket_bp.tickets')

        return redirect(redirect_url)

    sort = request.args.get('sort')
    if sort:
        args = request.args.copy()
        del args['sort']

        response = make_response(redirect(url_for('flicket_bp.tickets', **args)))
        response.set_cookie('tickets_sort', sort, max_age=2419200, path=url_for('flicket_bp.tickets'))

        return response

    sort = request.cookies.get('tickets_sort')
    if sort:
        set_cookie = True
    else:
        sort = 'priority_desc'
        set_cookie = False

    ticket_query, form = FlicketTicket.query_tickets(form, department=department, category=category, status=status,
                                                     user_id=user_id, content=content)
    ticket_query = FlicketTicket.sorted_tickets(ticket_query, sort)
    number_results = ticket_query.count()

    ticket_query = ticket_query.paginate(page, app.config['posts_per_page'])

    title = gettext('Tickets')

    # todo: pull from api on page load as other fields?
    if content:
        form.content.data = content

    response = make_response(render_template('flicket_tickets.html',
                                             title=title,
                                             form=form,
                                             tickets=ticket_query,
                                             page=page,
                                             number_results=number_results,
                                             status=status,
                                             department=department,
                                             category=category,
                                             user_id=user_id,
                                             sort=sort,
                                             base_url='flicket_bp.tickets'))

    if set_cookie:
        response.set_cookie('tickets_sort', sort, max_age=2419200, path=url_for('flicket_bp.tickets'))

    return response


@flicket_bp.route(app.config['FLICKET'] + 'tickets_csv/', methods=['GET', 'POST'])
@login_required
def tickets_csv():
    # get request arguments from the url
    status = request.args.get('status')
    department = request.args.get('department')
    category = request.args.get('category')
    content = request.args.get('content')
    user_id = request.args.get('user_id')

    ticket_query, form = FlicketTicket.query_tickets(department=department, category=category, status=status,
                                                     user_id=user_id, content=content)
    ticket_query = ticket_query.limit(app.config['csv_dump_limit'])

    date_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = date_stamp + 'ticketdump.csv'

    csv_contents = 'Ticket_ID,Priority,Title,Submitted By,Date,Replies,Category,Status,Assigned,URL\n'
    for ticket in ticket_query:

        if hasattr(ticket.assigned, 'name'):
            _name = ticket.assigned.name
        else:
            _name = 'Not assigned'

        csv_contents += '{},{},"{}",{},{},{},{} - {},{},{},{}{}\n'.format(ticket.id_zfill,
                                                                          ticket.ticket_priority.priority,
                                                                          clean_csv_data(ticket.title),
                                                                          ticket.user.name,
                                                                          ticket.date_added.strftime("%Y-%m-%d"),
                                                                          ticket.num_replies,
                                                                          clean_csv_data(
                                                                              ticket.category.department.department),
                                                                          clean_csv_data(ticket.category.category),
                                                                          ticket.current_status.status,
                                                                          _name,
                                                                          app.config["base_url"],
                                                                          url_for("flicket_bp.ticket_view",
                                                                                  ticket_id=ticket.id))

    return Response(
        csv_contents,
        mimetype='text/csv',
        headers={"Content-disposition":
                 f"attachment; filename={file_name}"}
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
        redirect_url = FlicketTicket.form_redirect(form, url='flicket_bp.my_tickets')

        return redirect(redirect_url)

    sort = request.args.get('sort')
    if sort:
        args = request.args.copy()
        del args['sort']

        response = make_response(redirect(url_for('flicket_bp.my_tickets', **args)))
        response.set_cookie('my_tickets_sort', sort, max_age=2419200, path=url_for('flicket_bp.my_tickets'))

        return response

    sort = request.cookies.get('my_tickets_sort')
    if sort:
        set_cookie = True
    else:
        sort = 'priority_desc'
        set_cookie = False

    ticket_query, form = FlicketTicket.query_tickets(form, department=department, category=category, status=status,
                                                     user_id=user_id, content=content)
    ticket_query = FlicketTicket.my_tickets(ticket_query)
    ticket_query = FlicketTicket.sorted_tickets(ticket_query, sort)
    number_results = ticket_query.count()

    ticket_query = ticket_query.paginate(page, app.config['posts_per_page'])

    title = gettext('My Tickets')

    response = make_response(render_template('flicket_tickets.html',
                                             title=title,
                                             form=form,
                                             tickets=ticket_query,
                                             page=page,
                                             number_results=number_results,
                                             status=status,
                                             department=department,
                                             category=category,
                                             user_id=user_id,
                                             sort=sort,
                                             base_url='flicket_bp.my_tickets'))

    if set_cookie:
        response.set_cookie('my_tickets_sort', sort, max_age=2419200, path=url_for('flicket_bp.my_tickets'))

    return response
