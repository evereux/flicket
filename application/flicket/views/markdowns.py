#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import render_template

from . import flicket_bp
from application import app


# to do mark down view
@flicket_bp.route(app.config['FLICKET'] + 'todo/')
def todo():
    with open('TODO.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket_markdown.html', **locals())


# faq mark down view
@flicket_bp.route(app.config['FLICKET'] + 'faq/')
def faq():
    with open('FAQ.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket_markdown.html', **locals())
