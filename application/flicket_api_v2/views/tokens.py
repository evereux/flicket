#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import g, jsonify

from application import app, db
from application.flicket_api_v2.views import bp_api_v2
from application.flicket_api_v2.views.auth import basic_auth, token_auth


@bp_api_v2.route(app.config['FLICKET_API_V2'] + 'tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp_api_v2.route(app.config['FLICKET_API_V2'] + 'tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
