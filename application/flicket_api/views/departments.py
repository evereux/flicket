#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request, url_for

from . import bp_api

from application import app, db
from application.flicket.models.flicket_models import FlicketDepartment
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(app.config['FLICKET_API'] + 'department/<int:id>', methods=['GET'])
@token_auth.login_required
def get_department(id):
    return jsonify(FlicketDepartment.query.order_by(FlicketDepartment.department.asc()).get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'departments/', methods=['GET'])
@token_auth.login_required
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketDepartment.to_collection_dict(FlicketDepartment.query.order_by(FlicketDepartment.department.asc()),
                                                page, per_page, 'bp_api.get_departments')
    return jsonify(data)


@bp_api.route(app.config['FLICKET_API'] + 'departments', methods=['POST'])
@token_auth.login_required
def create_department():
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
