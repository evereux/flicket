import datetime
import decimal
import json

from flask import request
from flask_login import login_required

from application import app
from application.admin.models.user import User
from . import flicket_bp


def alchemyencoder(obj):
    """
    JSON enncoder function for sQLAlchemy special cases.
    Take from: http://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
    """
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


# tickets main
@flicket_bp.route(app.config['FLICKETHOME'] + 'api/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKETHOME'] + 'api/<r_db>/', methods=['GET', 'POST'])
@login_required
def api_query(r_db=None):

    filter = request.args.get('filter')

    json_dump = ''

    if r_db == 'users':
        query = User.query

        if filter:
            query = query.filter(User.username.ilike('%{}%'.format(filter)))

        listy = []
        for u in query:
            sub_dict = {
                'id': u.id,
                'username': u.username,
                'email_': u.email,
                'name': u.name
            }
            listy.append(sub_dict)

        json_dump = json.dumps(listy)




    return(json_dump)