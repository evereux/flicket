#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import g, jsonify, request, url_for

from . import bp_api

from application import app, db
from application.flicket.models.flicket_models import FlicketPriority, FlicketTicket, FlicketCategory
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(app.config['FLICKET_API'] + 'ticket/<int:id>', methods=['GET'])
@token_auth.login_required
def get_ticket(id):
    return jsonify(FlicketTicket.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'tickets/', methods=['GET'])
@bp_api.route(app.config['FLICKET_API'] + 'tickets/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_tickets(page=1):
    # todo: add filtering

    tickets = FlicketTicket.query
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketTicket.to_collection_dict(tickets, page, per_page, 'bp_api.get_tickets')
    return jsonify(data)


@bp_api.route(app.config['FLICKET_API'] + 'tickets', methods=['POST'])
@token_auth.login_required
def create_ticket():
    data = request.get_json() or {}

    if 'title' not in data or 'content' not in data or 'category_id' not in data or 'ticket_priority_id' not in data:
        return bad_request('Must include title, content, category_id and ticket_priority_id.')

    if not isinstance(data['category_id'], int) or not isinstance(data['ticket_priority_id'], int):
        return bad_request('ticket_priority_id and category_id must be integers.')

    if not FlicketCategory.query.filter_by(id=data['category_id']).first():
        return bad_request('not a valid category_id')

    if not FlicketPriority.query.filter_by(id=data['ticket_priority_id']).first():
        return bad_request('not a valid ticket_priority_id')

    ticket = FlicketTicket()
    ticket.from_dict(data)
    ticket.started_id = g.current_user.id
    ticket.date_added = datetime.datetime.now()
    ticket.status_id = 1

    db.session.add(ticket)
    db.session.commit()

    response = jsonify(ticket.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('bp_api.get_ticket', id=ticket.id)

    return response


@bp_api.route(app.config['FLICKET_API'] + 'priority/<int:id>', methods=['GET'])
@token_auth.login_required
def get_priority(id):
    return jsonify(FlicketPriority.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'priorities/', methods=['GET'])
@bp_api.route(app.config['FLICKET_API'] + 'priorities/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_priorities(page=1):
    priorities = FlicketPriority.query
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketPriority.to_collection_dict(priorities, page, per_page, 'bp_api.get_priorities')
    return jsonify(data)
