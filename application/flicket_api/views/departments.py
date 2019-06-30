#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Departments
    ===========

    Get Department by ID
    ~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/department/(int:department_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/department/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 191
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:37:21 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "department": "Design",
                "id": 1,
                "links": {
                    "departments": "http://127.0.0.1:5000/flicket-api/departments/",
                    "self": "http://127.0.0.1:5000/flicket-api/department/1"
                }
            }

    Get Departments
    ~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/departments/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/departments/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 2307
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:40:21 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/departments/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 9,
                    "total_pages": 1
                },
                "items": [
                    {
                        "department": "Commercial",
                        "id": 6,
                        "links": {
                            "departments": "http://127.0.0.1:5000/flicket-api/departments/",
                            "self": "http://127.0.0.1:5000/flicket-api/department/6"
                        }
                    },
                    {
                        "department": "Design",
                        "id": 1,
                        "links": {
                            "departments": "http://127.0.0.1:5000/flicket-api/departments/",
                            "self": "http://127.0.0.1:5000/flicket-api/department/1"
                        }
                    },
                    {
                        "department": "Human Resources",
                        "id": 5,
                        "links": {
                            "departments": "http://127.0.0.1:5000/flicket-api/departments/",
                            "self": "http://127.0.0.1:5000/flicket-api/department/5"
                        }
                    },
                    {
                        "department": "IT",
                        "id": 3,
                        "links": {
                            "departments": "http://127.0.0.1:5000/flicket-api/departments/",
                            "self": "http://127.0.0.1:5000/flicket-api/department/3"
                        }
                    }
                ]
            }


    Create Department
    ~~~~~~~~~~~~~~~~~

    .. http:post:: http://localhost:5000/flicket-api/departments(str:department)

        **Request**

        .. sourcecode:: http

            POST /flicket-api/departments HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

            {
                "department": "new department"
            }

        **Response**

        .. sourcecode: http::

            HTTP/1.0 201 CREATED
            Content-Length: 201
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:45:35 GMT
            Location: http://localhost:5000/flicket-api/department/12
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "department": "New Department",
                "id": 12,
                "links": {
                    "departments": "http://127.0.0.1:5000/flicket-api/departments/",
                    "self": "http://127.0.0.1:5000/flicket-api/department/12"
                }
            }
"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketDepartment
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + 'department/<int:id>', methods=['GET'])
@token_auth.login_required
def get_department(id):
    return jsonify(FlicketDepartment.query.order_by(FlicketDepartment.department.asc()).get_or_404(id).to_dict())


@bp_api.route(api_url + 'departments/', methods=['GET'])
@token_auth.login_required
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketDepartment.to_collection_dict(FlicketDepartment.query.order_by(FlicketDepartment.department.asc()),
                                                page, per_page, 'bp_api.get_departments')
    return jsonify(data)


@bp_api.route(api_url + 'departments', methods=['POST'])
@token_auth.login_required
def create_department():

    # todo add authentication. only those in the admin or super_user groups should be allowed to create.

    data = request.get_json() or {}

    if 'department' not in data:
        return bad_request('Must include department name.')

    if FlicketDepartment.query.filter_by(department=data['department']).first():
        return bad_request('Department already created.')

    department = FlicketDepartment(data['department'])
    db.session.add(department)
    db.session.commit()

    response = jsonify(department.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('bp_api.get_department', id=department.id)

    return response
