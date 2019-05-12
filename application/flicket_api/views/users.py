#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api
from application import app
from application.flicket.models.flicket_user import FlicketUser
from application.flicket_api.views.auth import token_auth


@bp_api.route(app.config['FLICKET_API'] + 'user/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(FlicketUser.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'users/', methods=['GET'])
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
