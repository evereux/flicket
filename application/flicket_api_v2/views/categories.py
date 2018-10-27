#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api_v2

from application import app
from application.flicket.models.flicket_models import FlicketCategory, FlicketDepartment
from application.flicket_api_v2.views.auth import token_auth


@bp_api_v2.route(app.config['FLICKET_API_V2'] + 'category/<int:id>', methods=['GET'])
@token_auth.login_required
def get_category(id_):
    return jsonify(FlicketCategory.query.get_or_404(id_).to_dict())


@bp_api_v2.route(app.config['FLICKET_API_V2'] + 'categories/', methods=['GET'])
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
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = FlicketCategory.to_collection_dict(categories, page, per_page, 'bp_api_v2.get_categories')
    return jsonify(data)

