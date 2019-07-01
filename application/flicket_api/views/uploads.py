#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Uploads
    =======

    Get Upload By ID
    ~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/upload/(int:upload_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/upload/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>


        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 415
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:46:54 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "filename": "ccv4ufb6.jpg",
                "id": 1,
                "image": "http://127.0.0.1:5000/flicket_uploads/ccv4ufb6.jpg",
                "links": {
                    "post": "http://127.0.0.1:5000/flicket-api/post/276646",
                    "self": "http://127.0.0.1:5000/flicket-api/upload/1",
                    "ticket": null,
                    "uploads": "http://127.0.0.1:5000/flicket-api/uploads/"
                },
                "original_filename": "photos-1.jpg",
                "post_id": 276646,
                "topic_id": null
            }


    Get Uploads
    ~~~~~~~~~~~

    .. http:get:: /flicket-api/uploads/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/uploads/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 1231
            Content-Type: application/json
            Date: Mon, 01 Jul 2019 11:49:33 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/uploads/1/?per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 2,
                    "total_pages": 1
                },
                "items": [
                    {
                        "filename": "ccv4ufb6.jpg",
                        "id": 1,
                        "image": "http://127.0.0.1:5000/flicket_uploads/ccv4ufb6.jpg",
                        "links": {
                            "post": "http://127.0.0.1:5000/flicket-api/post/276646",
                            "self": "http://127.0.0.1:5000/flicket-api/upload/1",
                            "ticket": null,
                            "uploads": "http://127.0.0.1:5000/flicket-api/uploads/"
                        },
                        "original_filename": "photos-1.jpg",
                        "post_id": 276646,
                        "topic_id": null
                    },
                    {
                        "filename": "5w0hdo10.jpg",
                        "id": 2,
                        "image": "http://127.0.0.1:5000/flicket_uploads/5w0hdo10.jpg",
                        "links": {
                            "post": "http://127.0.0.1:5000/flicket-api/post/276677",
                            "self": "http://127.0.0.1:5000/flicket-api/upload/2",
                            "ticket": null,
                            "uploads": "http://127.0.0.1:5000/flicket-api/uploads/"
                        },
                        "original_filename": "the_basta_rock_sunrise_4k-wallpaper-3554x1999.jpg",
                        "post_id": 276677,
                        "topic_id": null
                    }
                ]
            }

"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketUploads
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'upload/<int:id>', methods=['GET'])
@token_auth.login_required
def get_upload(id):
    return jsonify(FlicketUploads.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'uploads/', methods=['GET'])
@bp_api.route(api_url + 'uploads/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_uploads(page=1):
    # todo: add filtering

    uploads = FlicketUploads.query
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketUploads.to_collection_dict(uploads, page, per_page, 'bp_api.get_uploads')
    return jsonify(data)
