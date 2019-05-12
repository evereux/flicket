#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request, url_for

from . import bp_api

from application import app, db
from application.flicket.models.flicket_models import FlicketCategory, FlicketDepartment
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(app.config['FLICKET_API'] + 'category/<int:id>', methods=['GET'])
@token_auth.login_required
def get_category(id):
    return jsonify(FlicketCategory.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'categories/', methods=['GET'])
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


@bp_api.route(app.config['FLICKET_API'] + 'categories', methods=['POST'])
@token_auth.login_required
def create_category():
    data = request.get_json() or {}

    if 'category' not in data or 'department_id' not in data:
        return bad_request('Must include category name and department_id')

    if not isinstance(data['department_id'], int):
        return bad_request('department_id must be an integer.')

    if FlicketCategory.query.filter_by(category=data['category']).filter_by(department_id=data['department_id']).first():
        return bad_request('Category within department already exists.')

    department = FlicketDepartment.query.filter_by(id=data['department_id']).first()
    category = FlicketCategory(data['category'], department)
    db.session.add(category)
    db.session.commit()

    response = jsonify(category.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('bp_api.get_category', id=category.id)
    return response
