#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import g, jsonify

from application import app, db
from application.flicket_api.views import bp_api
from application.flicket_api.views.auth import basic_auth, token_auth


@bp_api.route(app.config['FLICKET_API'] + 'tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp_api.route(app.config['FLICKET_API'] + 'tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
