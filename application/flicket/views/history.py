#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import render_template
from flask_babel import gettext
from flask_login import login_required

from application import app, flicket_bp
from application.flicket.models.flicket_models import FlicketHistory, FlicketPost, FlicketTicket


@flicket_bp.route(app.config['FLICKET'] + 'history/topic/<int:topic_id>/', methods=['GET', 'POST'])
@login_required
def flicket_history_topic(topic_id):

    history = FlicketHistory.query.filter_by(topic_id=topic_id).all()
    ticket = FlicketTicket.query.filter_by(id=topic_id).one()

    title = gettext('History')

    return render_template(
        'flicket_history.html',
        title=title,
        history=history,
        ticket=ticket)


@flicket_bp.route(app.config['FLICKET'] + 'history/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def flicket_history_post(post_id):

    history = FlicketHistory.query.filter_by(post_id=post_id).all()

    # get the ticket object so we can generate a url to link back to topic.
    post = FlicketPost.query.filter_by(id=post_id).one()
    ticket = FlicketTicket.query.filter_by(id=post.ticket_id).one()

    title = gettext('History')

    return render_template(
        'flicket_history.html',
        title=title,
        history=history,
        ticket=ticket)
