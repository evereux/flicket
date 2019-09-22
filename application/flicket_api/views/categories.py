#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Categories
    ==========

    Get Category By ID
    ~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/category/(int:category_id)

        **Request**

        .. sourcecode:: http

            GET /flicket-api/category/1 HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 282
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:55:57 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "category": "Dataset",
                "department": "Design",
                "id": 1,
                "links": {
                    "categories": "http://127.0.0.1:5000/flicket-api/categories/",
                    "department": "http://127.0.0.1:5000/flicket-api/department/1",
                    "self": "http://127.0.0.1:5000/flicket-api/category/1"
                }
            }

    Get Categories
    ~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/categories/

        **Request**

        .. sourcecode:: http

            GET /flicket-api/categories/ HTTP/1.1
            HOST: localhost:5000
            Accept: application/json
            Authorization: Bearer <token>

        **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Length: 5192
            Content-Type: application/json
            Date: Sun, 30 Jun 2019 12:51:02 GMT
            Server: Werkzeug/0.14.1 Python/3.7.3

            {
                "_links": {
                    "next": null,
                    "prev": null,
                    "self": "http://127.0.0.1:5000/flicket-api/categories/?page=1&per_page=50"
                },
                "_meta": {
                    "page": 1,
                    "per_page": 50,
                    "total_items": 15,
                    "total_pages": 1
                },
                "items": [
                    {
                        "category": "Approved Suppliers",
                        "department": "Commercial",
                        "id": 14,
                        "links": {
                            "categories": "http://127.0.0.1:5000/flicket-api/categories/",
                            "department": "http://127.0.0.1:5000/flicket-api/department/6",
                            "self": "http://127.0.0.1:5000/flicket-api/category/14"
                        }
                    },
                    {
                        "category": "Dataset",
                        "department": "Design",
                        "id": 1,
                        "links": {
                            "categories": "http://127.0.0.1:5000/flicket-api/categories/",
                            "department": "http://127.0.0.1:5000/flicket-api/department/1",
                            "self": "http://127.0.0.1:5000/flicket-api/category/1"
                        }
                    },
                    {
                        "category": "ECR",
                        "department": "Design",
                        "id": 3,
                        "links": {
                            "categories": "http://127.0.0.1:5000/flicket-api/categories/",
                            "department": "http://127.0.0.1:5000/flicket-api/department/1",
                            "self": "http://127.0.0.1:5000/flicket-api/category/3"
                        }
                    },
                    {
                        "category": "Holidays",
                        "department": "Human Resources",
                        "id": 12,
                        "links": {
                            "categories": "http://127.0.0.1:5000/flicket-api/categories/",
                            "department": "http://127.0.0.1:5000/flicket-api/department/5",
                            "self": "http://127.0.0.1:5000/flicket-api/category/12"
                        }
                    }
                ]
            }

"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketCategory, FlicketDepartment
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + 'category/<int:id>', methods=['GET'])
@token_auth.login_required
def get_category(id):
    return jsonify(FlicketCategory.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'categories/', methods=['GET'])
@token_auth.login_required
def get_categories():
    department_id = request.args.get('department_id')
    department = request.args.get('department')
    categories = FlicketCategory.query.order_by(FlicketCategory.category.asc())
    if department_id:
        categories = categories.filter_by(department_id=department_id)
    if department:
        categories = categories.filter(FlicketCategory.department.has(FlicketDepartment.department == department))
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketCategory.to_collection_dict(categories, page, per_page, 'bp_api.get_categories')
    return jsonify(data)


@bp_api.route(api_url + 'categories', methods=['POST'])
@token_auth.login_required
def create_category():
    data = request.get_json() or {}

    if 'category' not in data or 'department_id' not in data:
        return bad_request('Must include category name and department_id')

    if not isinstance(data['department_id'], int):
        return bad_request('department_id must be an integer.')

    if FlicketCategory.query. \
            filter_by(category=data['category']). \
            filter_by(department_id=data['department_id']).first():
        return bad_request('Category within department already exists.')

    department = FlicketDepartment.query.filter_by(id=data['department_id']).first()
    category = FlicketCategory(data['category'], department)
    db.session.add(category)
    db.session.commit()

    response = jsonify(category.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('bp_api.get_category', id=category.id)
    return response
