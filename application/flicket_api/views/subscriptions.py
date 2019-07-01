#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Subscriptions
    =============

    Get Subscription By ID
    ~~~~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/subscription/(int:subscription_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/subscription/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 356
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:21:57 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "id": 1,
                "links": {
                    "self": "http://127.0.0.1:5000/flicket-api/subscription/1",
                    "subscriptions": "http://127.0.0.1:5000/flicket-api/subscriptions/",
                    "ticket": "http://127.0.0.1:5000/flicket-api/ticket/10001",
                    "user": "http://127.0.0.1:5000/flicket-api/user/1"
                },
                "ticket_id": 10001,
                "user_def": "admin",
                "user_id": 1
            }


    Get Subscriptions
    ~~~~~~~~~~~~~~~~~

    Get all subscribers to ticket.

    .. http:get:: /flicket-api/subscriptions/(int:ticket_id)/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/users/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 666
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:27:12 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/subscriptions/10001/1/?per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 1,
                    "total_pages": 1
                },
                "items": [
                    {
                        "id": 1,
                        "links": {
                            "self": "http://127.0.0.1:5000/flicket-api/subscription/1",
                            "subscriptions": "http://127.0.0.1:5000/flicket-api/subscriptions/",
                            "ticket": "http://127.0.0.1:5000/flicket-api/ticket/10001",
                            "user": "http://127.0.0.1:5000/flicket-api/user/1"
                        },
                        "ticket_id": 10001,
                        "user_def": "admin",
                        "user_id": 1
                    }
                ]
            }

"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketSubscription
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'subscription/<int:id>', methods=['GET'])
@token_auth.login_required
def get_subscription(id):
    return jsonify(FlicketSubscription.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'subscriptions/', methods=['GET'])
@bp_api.route(api_url + 'subscriptions/<int:ticket_id>/', methods=['GET'])
@bp_api.route(api_url + 'subscriptions/<int:ticket_id>/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_subscriptions(page=1, ticket_id=None):
    subscriptions = FlicketSubscription.query
    if ticket_id:
        subscriptions = subscriptions.filter_by(ticket_id=ticket_id)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketSubscription.to_collection_dict(subscriptions, page, per_page, 'bp_api.get_subscriptions',
                                                  ticket_id=ticket_id)
    return jsonify(data)
