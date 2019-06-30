#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from .sphinx_helper import api_url
from . import bp_api
from application import app
from application.flicket.models.flicket_models import FlicketHistory
from application.flicket_api.views.auth import token_auth


@bp_api.route(api_url + 'history/<int:id>', methods=['GET'])
@token_auth.login_required
def get_history(id):
    return jsonify(FlicketHistory.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'histories/', methods=['GET'])
@bp_api.route(api_url + 'histories/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_histories(page=1):
    topic_id = request.args.get('topic_id')
    post_id = request.args.get('post_id')

    histories = FlicketHistory.query
    if topic_id:
        histories = histories.filter_by(topic_id=topic_id)
    if post_id:
        histories = histories.filter_by(post_id=post_id)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketHistory.to_collection_dict(histories, page, per_page, 'bp_api.get_histories', topic_id=topic_id)
    return jsonify(data)
