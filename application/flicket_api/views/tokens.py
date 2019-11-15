#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    Authentication / Tokens
    =======================

    Get Token
    ~~~~~~~~~

    The user will need to provide their username and password to retrieve an authentication token. The authentication
    token is required to access all other parts of the API.

    .. code-block::

        # example using httpie
        http --auth <username>:<password> POST http://localhost:5000/flicket-api/tokens

    **Response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Length: 50
        Content-Type: application/json
        Date: Sat, 29 Sep 2018 14:01:00 GMT
        Server: Werkzeug/0.14.1 Python/3.6.5

        {
            "token": "<token>"
        }


    Delete Token
    ~~~~~~~~~~~~

    .. code-block::

        # example using httpie
        http DELETE http://localhost:5000/flicket-api/tokens "Authorization: Bearer <token>"

    **Responds**

    .. sourcecode:: http

        HTTP/1.0 204 NO CONTENT
        Content-Length: 0
        Content-Type: text/html; charset=utf-8
        Date: Sat, 29 Sep 2018 14:13:19 GMT
        Server: Werkzeug/0.14.1 Python/3.6.5

"""

from flask import g, jsonify

from .sphinx_helper import api_url
from . import bp_api
from application import db
from application.flicket_api.views.auth import basic_auth, token_auth


@bp_api.route(api_url + 'tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp_api.route(api_url + 'tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
