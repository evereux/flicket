#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketAction
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'action/<int:id>', methods=['GET'])
@token_auth.login_required
def get_action(id):
    return jsonify(FlicketAction.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'actions/<int:ticket_id>', methods=['GET'])
@token_auth.login_required
def get_actions(ticket_id):
    actions = FlicketAction.query.filter_by(ticket_id=ticket_id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketAction.to_collection_dict(actions, page, per_page, 'bp_api.get_actions', ticket_id=ticket_id)
    return jsonify(data)
