#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import render_template
from flask_login import login_required

from . import flicket_bp
from application import app


# faq mark down view
@flicket_bp.route(app.config['FLICKET'] + 'faq/')
@login_required
def faq():
    with open('FAQ.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket_markdown.html', **locals())
