#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    Tickets
    =======

    Get Ticket By ID
    ~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/ticket/(int:ticket_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/ticket/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 1835
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 14:15:37 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "assigned_id": 7,
                "category_id": 1,
                "content": "She spent her earliest years reading classic literature, and writing poetry. Haskell
                features a type system with type inference and lazy evaluation. They are written as strings of
                consecutive alphanumeric characters, the first character being lowercase. Tuples are containers for
                a fixed number of Erlang data types. Erlang is a general-purpose, concurrent, functional programming
                language. Where are my pants? He looked inquisitively at his keyboard and wrote another sentence. The
                arguments can be primitive data types or compound data types. It is also a garbage-collected runtime
                system. He looked inquisitively at his keyboard and wrote another sentence. Do you come here often?
                Ports are created with the built-in function open_port. He looked inquisitively at his keyboard and
                wrote another sentence. Haskell features a type system with type inference and lazy evaluation.",
                "date_added": "Sun, 23 Jun 2019 18:25:36 GMT",
                "date_modified": null,
                "id": 1,
                "links": {
                    "assigned": "http://localhost:5000/flicket-api/user/7",
                    "category": "http://localhost:5000/flicket-api/category/1",
                    "histories": "http://localhost:5000/flicket-api/histories/?topic_id=1",
                    "modified_by": null,
                    "priority": "http://localhost:5000/flicket-api/priority/3",
                    "self": "http://localhost:5000/flicket-api/ticket/1",
                    "started_ny": "http://localhost:5000/flicket-api/user/12",
                    "status": "http://localhost:5000/flicket-api/status/2",
                    "subscribers": "http://localhost:5000/flicket-api/subscriptions/1/",
                    "tickets": "http://localhost:5000/flicket-api/tickets/"
                },
                "modified_id": null,
                "started_id": 12,
                "status_id": 2,
                "ticket_priority_id": 3,
                "title": "He looked inquisitively at his keyboard and wrote another sentence."
            }


    Get Tickets
    ~~~~~~~~~~~

        .. http:get:: /flicket-api/tickets/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/tickets/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 2244
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 14:15:37 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": "http://localhost:5000/flicket-api/tickets/2/?per_page=1",
                    "prev": null,
                    "self": "http://localhost:5000/flicket-api/tickets/1/?per_page=1"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 1,
                    "total_items": 10000,
                    "total_pages": 10000
                },
                "items": [
                    {
                        "assigned_id": 7,
                        "category_id": 1,
                        "content": "She spent her earliest years reading classic literature, and writing poetry. Haskell
                        features a type system with type inference and lazy evaluation. They are written as strings of
                        consecutive alphanumeric characters, the first character being lowercase. Tuples are containers
                        for a fixed number of Erlang data types. Erlang is a general-purpose, concurrent, functional
                        programming language. Where are my pants? He looked inquisitively at his keyboard and wrote
                        another sentence. The arguments can be primitive data types or compound data types. It is also a
                        garbage-collected runtime system. He looked inquisitively at his keyboard and wrote another
                        sentence. Do you come here often? Ports are created with the built-in function open_port. He
                        looked inquisitively at his keyboard and wrote another sentence. Haskell features a type system
                        with type inference and lazy evaluation.",
                        "date_added": "Sun, 23 Jun 2019 18:25:36 GMT",
                        "date_modified": null,
                        "id": 1,
                        "links": {
                            "assigned": "http://localhost:5000/flicket-api/user/7",
                            "category": "http://localhost:5000/flicket-api/category/1",
                            "histories": "http://localhost:5000/flicket-api/histories/?topic_id=1",
                            "modified_by": null,
                            "priority": "http://localhost:5000/flicket-api/priority/3",
                            "self": "http://localhost:5000/flicket-api/ticket/1",
                            "started_ny": "http://localhost:5000/flicket-api/user/12",
                            "status": "http://localhost:5000/flicket-api/status/2",
                            "subscribers": "http://localhost:5000/flicket-api/subscriptions/1/",
                            "tickets": "http://localhost:5000/flicket-api/tickets/"
                        },
                        "modified_id": null,
                        "started_id": 12,
                        "status_id": 2,
                        "ticket_priority_id": 3,
                        "title": "He looked inquisitively at his keyboard and wrote another sentence."
                    }
                ]
            }


    Create Ticket
    ~~~~~~~~~~~~~

    .. http:post:: /flicket-api/tickets(str:title,str:content,int:category_id,int:ticket_priority_id)

        **Request**

        .. sourcecode:: http

            POST /flicket-api/tickets HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

            {
                "title": "this is my ticket",
                "content": "this is my content",
                "category_id": 1,
                "ticket_priority_id": 1
            }

        **Response**

        .. sourcecode:: http

                HTTP/1.0 201 CREATED
                Content-Length: 903
                Content-Type: application/json
                Date: Fri, 28 Jun 2019 12:04:59 GMT
                Location: http://localhost:5000/flicket-api/ticket/10001
                Server: Werkzeug/0.14.1 Python/3.7.3

                {
                    "assigned_id": null,
                    "category_id": 1,
                    "content": "this is my content",
                    "date_added": "Fri, 28 Jun 2019 13:04:59 GMT",
                    "date_modified": null,
                    "id": 10001,
                    "links": {
                        "assigned": null,
                        "category": "http://localhost:5000/flicket-api/category/1",
                        "histories": "http://localhost:5000/flicket-api/histories/?topic_id=10001",
                        "modified_by": null,
                        "priority": "http://localhost:5000/flicket-api/priority/1",
                        "self": "http://localhost:5000/flicket-api/ticket/10001",
                        "started_ny": "http://localhost:5000/flicket-api/user/1",
                        "status": "http://localhost:5000/flicket-api/status/1",
                        "subscribers": "http://localhost:5000/flicket-api/subscriptions/10001/",
                        "tickets": "http://localhost:5000/flicket-api/tickets/"
                    },
                    "modified_id": null,
                    "started_id": 1,
                    "status_id": 1,
                    "ticket_priority_id": 1,
                    "title": "this is my ticket"
                }




"""

import datetime

from flask import g, jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketPriority, FlicketTicket, FlicketCategory
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + 'ticket/<int:id>', methods=['GET'])
@token_auth.login_required
def get_ticket(id):
    return jsonify(FlicketTicket.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'tickets/', methods=['GET'])
@bp_api.route(api_url + 'tickets/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_tickets(page=1):
    # todo: add filtering

    tickets = FlicketTicket.query
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketTicket.to_collection_dict(tickets, page, per_page, 'bp_api.get_tickets')
    return jsonify(data)


@bp_api.route(api_url + 'tickets', methods=['POST'])
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
