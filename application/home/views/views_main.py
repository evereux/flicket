#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import (render_template)

from application import app
from . import home_bp


# index page
@home_bp.route(app.config['WEBHOME'], methods=['GET'])
def index():
    return render_template('index.html', title='Flicket Ticket System')
