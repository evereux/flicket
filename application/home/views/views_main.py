#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import redirect, url_for

from application import app
from . import home_bp


# index page
@home_bp.route(app.config['WEBHOME'], methods=['GET'])
def index():
    return redirect(url_for('flicket_bp.index'))
