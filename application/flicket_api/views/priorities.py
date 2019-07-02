# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    Priorities
    ==========

    Get Priority By ID
    ~~~~~~~~~~~~~~~~~~

        .. http:get:: /flicket-api/priority/(int:priority_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/priority/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 182
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 14:15:37 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "id": 1,
                "links": {
                    "priorities": "http://127.0.0.1:5000/flicket-api/priorities/",
                    "self": "http://127.0.0.1:5000/flicket-api/priority/1"
                },
                "priority": "low"
            }


    Get Priorities
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/priorities/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/priorities/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

                HTTP/1.0 200 OK
                Content-Length: 903
                Content-Type: application/json
                Date: Sun, 30 Jun 2019 12:34:06 GMT
                Server: Werkzeug/0.14.1 Python/3.7.3

                {
                    "_links": {
                        "next": null,
                        "prev": null,
                        "self": "http://127.0.0.1:5000/flicket-api/priorities/1/?per_page=50"
                    },
                    "_meta": {
                        "page": 1,
                        "per_page": 50,
                        "total_items": 3,
                        "total_pages": 1
                    },
                    "items": [
                        {
                            "id": 1,
                            "links": {
                                "priorities": "http://127.0.0.1:5000/flicket-api/priorities/",
                                "self": "http://127.0.0.1:5000/flicket-api/priority/1"
                            },
                            "priority": "low"
                        },
                        {
                            "id": 2,
                            "links": {
                                "priorities": "http://127.0.0.1:5000/flicket-api/priorities/",
                                "self": "http://127.0.0.1:5000/flicket-api/priority/2"
                            },
                            "priority": "medium"
                        },
                        {
                            "id": 3,
                            "links": {
                                "priorities": "http://127.0.0.1:5000/flicket-api/priorities/",
                                "self": "http://127.0.0.1:5000/flicket-api/priority/3"
                            },
                            "priority": "high"
                        }
                    ]
                }

"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketPriority
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'priority/<int:id>', methods=['GET'])
@token_auth.login_required
def get_priority(id):
    return jsonify(FlicketPriority.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'priorities/', methods=['GET'])
@bp_api.route(api_url + 'priorities/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_priorities(page=1):
    priorities = FlicketPriority.query
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketPriority.to_collection_dict(priorities, page, per_page, 'bp_api.get_priorities')
    return jsonify(data)
