#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api

from application import app
from application.flicket.models.flicket_models import FlicketPost
from application.flicket_api.views.auth import token_auth


@bp_api.route(app.config['FLICKET_API'] + 'post/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    return jsonify(FlicketPost.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'posts/<int:ticket_id>/', methods=['GET'])
@bp_api.route(app.config['FLICKET_API'] + 'posts/<int:ticket_id>/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_posts(page=1, ticket_id=None):
    posts = FlicketPost.query.filter_by(ticket_id=ticket_id)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketPost.to_collection_dict(posts, page, per_page, 'bp_api.get_posts', ticket_id=ticket_id)
    return jsonify(data)
