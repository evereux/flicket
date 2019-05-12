#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import jsonify, request

from . import bp_api

from application import app
from application.flicket.models.flicket_models import FlicketUploads
from application.flicket_api.views.auth import token_auth


@bp_api.route(app.config['FLICKET_API'] + 'upload/<int:id>', methods=['GET'])
@token_auth.login_required
def get_upload(id):
    return jsonify(FlicketUploads.query.get_or_404(id).to_dict())


@bp_api.route(app.config['FLICKET_API'] + 'uploads/', methods=['GET'])
@bp_api.route(app.config['FLICKET_API'] + 'uploads/<int:page>/', methods=['GET'])
@token_auth.login_required
def uploads(page=1):
    # todo: add filtering

    uploads = FlicketUploads.query
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketUploads.to_collection_dict(uploads, page, per_page, 'bp_api.get_uploads')
    return jsonify(data)
