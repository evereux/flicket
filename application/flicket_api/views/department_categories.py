#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Department / Category
    =====================

    Get Department / Category By Category ID
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/department_category/(int:category_id)

    Get Department / Categories
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/department_categories/
"""

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketDepartmentCategory
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'department_category/<int:id>', methods=['GET'])
@token_auth.login_required
def get_department_category(id):
    return jsonify(FlicketDepartmentCategory.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'department_categories/', methods=['GET'])
@token_auth.login_required
def get_department_categories():
    department_category = request.args.get('department_category')
    department_id = request.args.get('department_id')
    department = request.args.get('department')
    department_categories = FlicketDepartmentCategory.query.order_by(FlicketDepartmentCategory.department_category)
    kwargs = {}
    if department_category:
        department_categories = department_categories.filter(
            FlicketDepartmentCategory.department_category.ilike(f'%{department_category}%'))
        kwargs['department_category'] = department_category
    if department_id:
        department_categories = department_categories.filter_by(department_id=department_id)
        kwargs['department_id'] = department_id
    if department:
        department_categories = department_categories.filter(
            FlicketDepartmentCategory.department.ilike(f'%{department}'))
        kwargs['department'] = department
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketDepartmentCategory.to_collection_dict(
        department_categories, page, per_page, 'bp_api.get_department_categories', **kwargs)
    return jsonify(data)
