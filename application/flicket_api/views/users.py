#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    Users
    =====

    Get User By ID
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/user/(int:user_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/user/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 355
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 14:15:37 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "avatar": "http://127.0.0.1:5000/flicket/static/flicket_avatars/5bxk0qxt.jpg",
                "email": "evereux@gmail.com",
                "id": 1,
                "job_title": "admin",
                "links": {
                    "self": "http://127.0.0.1:5000/flicket-api/user/1",
                    "users": "http://127.0.0.1:5000/flicket-api/users/"
                },
                "name": "admin",
                "total_posts": 12505,
                "username": "admin"
            }

    Get Users
    ~~~~~~~~~

    .. http:get:: /flicket-api/users/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/users/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 355
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 14:15:37 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://localhost:5000/flicket-api/users/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 48,
                    "total_pages": 1
                },
                "items": [
                    {
                        "avatar": "http://localhost:5000/flicket/static/flicket_avatars/__default_profile.png",
                        "email": "evereux@gmail.com",
                        "id": 1,
                        "job_title": "admin",
                        "links": {
                            "self": "http://localhost:5000/flicket-api/user/1",
                            "users": "http://localhost:5000/flicket-api/users/"
                        },
                        "name": "admin",
                        "total_posts": 6381,
                        "username": "admin"
                    },
                    {
                        "avatar": "http://localhost:5000/flicket/static/flicket_avatars/__default_profile.png",
                        "email": "admin@localhost",
                        "id": 2,
                        "job_title": "unknown",
                        "links": {
                            "self": "http://localhost:5000/flicket-api/user/2",
                            "users": "http://localhost:5000/flicket-api/users/"
                        },
                        "name": "notification",
                        "total_posts": 6445,
                        "username": "notification"
                    },
                ]
            }

"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_user import FlicketUser
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'user/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(FlicketUser.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'users/', methods=['GET'])
@token_auth.login_required
def get_users():
    name = request.args.get('name')
    users = FlicketUser.query
    if name:
        users = users.filter(FlicketUser.name.ilike('%{}%'.format(name)))
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketUser.to_collection_dict(users, page, per_page, 'bp_api.get_users')
    return jsonify(data)
