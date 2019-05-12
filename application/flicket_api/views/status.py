#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api

from application import app
from application.flicket.models.flicket_models import FlicketStatus
from application.flicket_api.views.auth import token_auth


@bp_api.route(app.config['FLICKET_API'] + 'status/<int:id>', methods=['GET'])
@token_auth.login_required
def get_status(id):
    return jsonify(FlicketStatus.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'statuses/', methods=['GET'])
@token_auth.login_required
def get_statuses():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketStatus.to_collection_dict(FlicketStatus.query, page, per_page, 'bp_api.get_departments')
    return jsonify(data)
