#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com


from flask import render_template
from flask_login import login_required

from . import flicket_bp
from application import app


# view users
@flicket_bp.route(app.config['FLICKET'] + 'markdown_primer/', methods=['GET', 'POST'])
@login_required
def markdown_primer():
    return render_template('markdown_primer.html')
