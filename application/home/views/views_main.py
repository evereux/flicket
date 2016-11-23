#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import (render_template)

from application import app
from . import home_bp


# used for debugging purposes only
def print_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print("Error in the {} field - {}".format(
                getattr(form, field).label.text,
                error
            ))


# index page
@home_bp.route(app.config['WEBHOME'], methods=['GET'])
def index():
    return render_template('index.html', title='Flicket Ticket System')
