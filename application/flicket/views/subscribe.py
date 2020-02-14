#! usr/bin/python3
# -*- coding: utf-8 -*-

# ! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import flash, g, redirect, url_for
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.models.flicket_models import FlicketTicket, FlicketSubscription
from application.flicket.scripts.flicket_functions import add_action
from . import flicket_bp


# view to subscribe user to a ticket.
@flicket_bp.route(app.config['FLICKET'] + 'subscribe/<int:ticket_id>/', methods=['GET', 'POST'])
@login_required
def subscribe_ticket(ticket_id=None):

    if ticket_id:

        ticket = FlicketTicket.query.filter_by(id=ticket_id).one()

        if not ticket.is_subscribed(g.user):
            # subscribe user to ticket
            subscribe = FlicketSubscription(user=g.user, ticket=ticket)
            ticket.last_updated = datetime.datetime.now()
            add_action(ticket, 'subscribe', recipient=g.user)
            db.session.add(subscribe)
            db.session.commit()
            flash(gettext('You have been subscribed to this ticket.'))

        else:

            flash(gettext('Already subscribed to this ticket'))

        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))


# view to unsubscribe user from a ticket.
@flicket_bp.route(app.config['FLICKET'] + 'unsubscribe/<int:ticket_id>/', methods=['GET', 'POST'])
@login_required
def unsubscribe_ticket(ticket_id=None):

    if ticket_id:

        ticket = FlicketTicket.query.filter_by(id=ticket_id).one()

        if ticket.is_subscribed(g.user):

            subscription = FlicketSubscription.query.filter_by(user=g.user, ticket=ticket).one()
            # unsubscribe user to ticket
            ticket.last_updated = datetime.datetime.now()
            add_action(ticket, 'unsubscribe', recipient=g.user)
            db.session.delete(subscription)
            db.session.commit()
            flash(gettext('You have been unsubscribed from this ticket.'))

        else:

            flash(gettext('You are already subscribed from this ticket'))

        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))
