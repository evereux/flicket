#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api

from application import app
from application.flicket.models.flicket_models import FlicketSubscription
from application.flicket_api.views.auth import token_auth


@bp_api.route(app.config['FLICKET_API'] + 'subscription/<int:id>', methods=['GET'])
@token_auth.login_required
def get_subscription(id):
    return jsonify(FlicketSubscription.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'subscriptions/', methods=['GET'])
@bp_api.route(app.config['FLICKET_API'] + 'subscriptions/<int:ticket_id>/', methods=['GET'])
@bp_api.route(app.config['FLICKET_API'] + 'subscriptions/<int:ticket_id>/<int:page>/', methods=['GET'])
@token_auth.login_required
def get_subscriptions(page=1, ticket_id=None):
    subscriptions = FlicketSubscription.query
    if ticket_id:
        subscriptions = subscriptions.filter_by(ticket_id=ticket_id)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketSubscription.to_collection_dict(subscriptions, page, per_page, 'bp_api.get_subscriptions',
                                                  ticket_id=ticket_id)
    return jsonify(data)
