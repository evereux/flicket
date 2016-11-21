import datetime
import os

from flask import render_template

from application import app


# to do mark down view
@app.route(app.config['FLICKETHOME'] + 'todo/')
def todo():

    with open('TODO.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket/flicket_markdown.html', **locals())


# faq mark down view
@app.route(app.config['FLICKETHOME'] + 'faq/')
def faq():

    with open('FAQ.md', 'r') as myfile:
        content = myfile.read()

    return render_template('flicket/flicket_markdown.html', **locals())
