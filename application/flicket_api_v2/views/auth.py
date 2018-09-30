#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

'''

    To get a token with httpie
    http --auth <username>:<password> POST http://localhost:5000/flicket-api-v2/tokens

    HTTP/1.0 200 OK
    Content-Length: 50
    Content-Type: application/json
    Date: Sat, 29 Sep 2018 14:01:00 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

    {
        "token": "< token >"
    }


    To retrieve a page requiring login with httpie:
    http http://localhost:5000/flicket-api-v2/user/1 "Authorization: Bearer <token>"

    HTTP/1.0 200 OK
    Content-Length: 203
    Content-Type: application/json
    Date: Sat, 29 Sep 2018 14:02:44 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

    {
        "email": "< email >",
        "id": 1,
        "job_title": "< job_title >",
        "links": {
            "self": "/flicket-api-v2/user/1"
        },
        "name": "< name >",
        "total_posts": < total_posts >,
        "username": "<username>"
    }


    To delete the token
    http DELETE http://localhost:5000/flicket-api-v2/tokens "Authorization: Bearer < token >"

    HTTP/1.0 204 NO CONTENT
    Content-Length: 0
    Content-Type: text/html; charset=utf-8
    Date: Sat, 29 Sep 2018 14:13:19 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

'''

from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from application.flicket.models.flicket_user import FlicketUser
from application.flicket_api_v2.views.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = FlicketUser.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = FlicketUser.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)
