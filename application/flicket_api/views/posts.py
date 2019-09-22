#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Posts
    =====

    Get Post By ID
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/post/(int:post_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/priority/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 1231
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 13:00:13 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "content": "The Galactic Empire is nearing completion of the Death Star, a space station with the power
                 to destroy entire planets. Initially ...",
                "data_added": "Sun, 05 May 2019 14:19:42 GMT",
                "date_modified": null,
                "id": 1,
                "links": {
                    "created_by": "http://127.0.0.1:5000/flicket-api/user/15",
                    "posts": "http://127.0.0.1:5000/flicket-api/posts/1/",
                    "self": "http://127.0.0.1:5000/flicket-api/post/1"
                },
                "ticket_id": 1,
                "user_id": 15
            }


    Get Posts
    ~~~~~~~~~

    Retrieve all posts associated to a ticket by ticket_id.

    .. http:get:: /flicket-api/posts/(int:ticket_id)/(int:page)/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/posts/1/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 27640
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 15:41:09 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/posts/1/1/?per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 25,
                    "total_pages": 1
                },
                "items": [
                    {
                        "content": "The Galactic Empire is nearing completion of the Death Star, a space station with
                        the power to destroy entire planets. Initially composing light-hearted and irreverent works,
                        he also wrote serious, sombre and religious pieces beginning in the 1930s. Erlang is known for
                        its designs that are well suited for systems. It is also a garbage-collected runtime system.
                        They are written as strings of consecutive alphanumeric characters, the first character being
                        lowercase. The sequential subset of Erlang supports eager evaluation, single assignment, and
                        dynamic typing. Tuples are containers for a fixed number of Erlang data types. Tuples are
                        containers for a fixed number of Erlang data types. The arguments can be primitive data types
                        or compound data types. Type classes first appeared in the Haskell programming language. The
                        arguments can be primitive data types or compound data types.",
                        "data_added": "Sun, 05 May 2019 14:19:42 GMT",
                        "date_modified": null,
                        "id": 1,
                        "links": {
                            "created_by": "http://127.0.0.1:5000/flicket-api/user/15",
                            "posts": "http://127.0.0.1:5000/flicket-api/posts/1/",
                            "self": "http://127.0.0.1:5000/flicket-api/post/1"
                        },
                        "ticket_id": 1,
                        "user_id": 15
                    }
                ]
            }
"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketPost
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'post/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    return jsonify(FlicketPost.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'posts/<int:ticket_id>/', methods=['GET'])
@bp_api.route(api_url + 'posts/<int:ticket_id>/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_posts(page=1, ticket_id=None):
    posts = FlicketPost.query.filter_by(ticket_id=ticket_id)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketPost.to_collection_dict(posts, page, per_page, 'bp_api.get_posts', ticket_id=ticket_id)
    return jsonify(data)
