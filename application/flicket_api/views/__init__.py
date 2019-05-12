#! python3
# -*- coding: utf-8 -*-#
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    To get a token with httpie. Some special characters will need to be escaped.
    http --auth <username>:<password> POST http://localhost:5000/flicket-api/tokens

    HTTP/1.0 200 OK
    Content-Length: 50
    Content-Type: application/json
    Date: Sat, 29 Sep 2018 14:01:00 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

    {
        "token": "< token >"
    }


    To retrieve a page requiring login with httpie:
    http http://localhost:5000/flicket-api/user/1 "Authorization: Bearer <token>"

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
            "self": "/flicket-api/user/1"
        },
        "name": "< name >",
        "total_posts": < total_posts >,
        "username": "<username>"
    }


    To delete the token
    http DELETE http://localhost:5000/flicket-api/tokens "Authorization: Bearer < token >"

    HTTP/1.0 204 NO CONTENT
    Content-Length: 0
    Content-Type: text/html; charset=utf-8
    Date: Sat, 29 Sep 2018 14:13:19 GMT
    Server: Werkzeug/0.14.1 Python/3.6.5

"""

from flask import Blueprint

bp_api = Blueprint('bp_api', __name__)
