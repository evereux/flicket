import datetime
import os

from flask import render_template

from . import flicket_bp
from application import app


# to do mark down view
@flicket_bp.route(app.config['FLICKETHOME'] + 'todo/')
def todo():

    with open('TODO.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket_markdown.html', **locals())


# faq mark down view
@flicket_bp.route(app.config['FLICKETHOME'] + 'faq/')
def faq():

    with open('FAQ.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket_markdown.html', **locals())
