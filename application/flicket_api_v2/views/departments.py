#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api_v2

from application import app
from application.flicket.models.flicket_models import FlicketDepartment
from application.flicket_api_v2.views.auth import token_auth


@bp_api_v2.route(app.config['FLICKET_API_V2'] + 'department/<int:id>', methods=['GET'])
@token_auth.login_required
def get_department(id_):
    return jsonify(FlicketDepartment.query.order_by(FlicketDepartment.department.asc()).get_or_404(id_).to_dict())


@bp_api_v2.route(app.config['FLICKET_API_V2'] + 'departments/', methods=['GET'])
@token_auth.login_required
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = FlicketDepartment.to_collection_dict(FlicketDepartment.query.order_by(FlicketDepartment.department.asc()),
                                                page, per_page, 'bp_api_v2.get_departments')
    return jsonify(data)
