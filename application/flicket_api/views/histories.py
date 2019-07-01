#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    History
    =======

    Ticket / Post edit history

    Get History By ID
    ~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/history/(int:history_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/history/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 456
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:52:33 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "date_modified": "Thu, 09 May 2019 17:17:58 GMT",
                "id": 1,
                "links": {
                    "histories": "http://127.0.0.1:5000/flicket-api/histories/",
                    "post": "http://127.0.0.1:5000/flicket-api/post/276645",
                    "self": "http://127.0.0.1:5000/flicket-api/history/1",
                    "ticket": null,
                    "user": "http://127.0.0.1:5000/flicket-api/user/1"
                },
                "original_content": "this is a reply\r\n",
                "post_id": 276645,
                "topic_id": null,
                "user_id": 1
            }


    Get Histories
    ~~~~~~~~~~~~~

    .. http:get:: /flicket-api/histories/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/histories/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 1786
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:53:39 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/histories/1/?per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 3,
                    "total_pages": 1
                },
                "items": [
                    {
                        "date_modified": "Thu, 09 May 2019 17:17:58 GMT",
                        "id": 1,
                        "links": {
                            "histories": "http://127.0.0.1:5000/flicket-api/histories/",
                            "post": "http://127.0.0.1:5000/flicket-api/post/276645",
                            "self": "http://127.0.0.1:5000/flicket-api/history/1",
                            "ticket": null,
                            "user": "http://127.0.0.1:5000/flicket-api/user/1"
                        },
                        "original_content": "this is a reply\r\n",
                        "post_id": 276645,
                        "topic_id": null,
                        "user_id": 1
                    },
                    {
                        "date_modified": "Fri, 10 May 2019 13:50:58 GMT",
                        "id": 2,
                        "links": {
                            "histories": "http://127.0.0.1:5000/flicket-api/histories/",
                            "post": null,
                            "self": "http://127.0.0.1:5000/flicket-api/history/2",
                            "ticket": "http://127.0.0.1:5000/flicket-api/ticket/10002",
                            "user": "http://127.0.0.1:5000/flicket-api/user/1"
                        },
                        "original_content": "\\sdv\\svd",
                        "post_id": null,
                        "topic_id": 10002,
                        "user_id": 1
                    },
                    {
                        "date_modified": "Wed, 22 May 2019 19:05:14 GMT",
                        "id": 3,
                        "links": {
                            "histories": "http://127.0.0.1:5000/flicket-api/histories/",
                            "post": "http://127.0.0.1:5000/flicket-api/post/276670",
                            "self": "http://127.0.0.1:5000/flicket-api/history/3",
                            "ticket": null,
                            "user": "http://127.0.0.1:5000/flicket-api/user/24"
                        },
                        "original_content": "zedrbzrb",
                        "post_id": 276670,
                        "topic_id": null,
                        "user_id": 24
                    }
                ]
            }


"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketHistory
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'history/<int:id>', methods=['GET'])
@token_auth.login_required
def get_history(id):
    return jsonify(FlicketHistory.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'histories/', methods=['GET'])
@bp_api.route(api_url + 'histories/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_histories(page=1):
    topic_id = request.args.get('topic_id')
    post_id = request.args.get('post_id')

    histories = FlicketHistory.query
    if topic_id:
        histories = histories.filter_by(topic_id=topic_id)
    if post_id:
        histories = histories.filter_by(post_id=post_id)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketHistory.to_collection_dict(histories, page, per_page, 'bp_api.get_histories', topic_id=topic_id)
    return jsonify(data)
