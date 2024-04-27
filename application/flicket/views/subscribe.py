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
from flask import abort
from flask import render_template

from application import app, db
from application.flicket.forms.flicket_forms import UnSubscribeUser
from application.flicket.models.flicket_models import FlicketSubscription
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_functions import add_action
from . import flicket_bp


# # view to unsubscribe user from a ticket.
# @flicket_bp.route(app.config['FLICKET'] + 'unsubscribe/<int:ticket_id>/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# def unsubscribe_ticket(ticket_id=None, user_id=None):
#     if ticket_id and user_id:
#
#         ticket = FlicketTicket.query.filter_by(id=ticket_id).one()
#         user = FlicketUser.query.filter_by(id=user_id).one()
#
#         if ticket.can_unsubscribe(user):
#             subscription = FlicketSubscription.query.filter_by(user=user, ticket=ticket).one()
#             # unsubscribe user to ticket
#             ticket.last_updated = datetime.datetime.now()
#             add_action(ticket, 'unsubscribe', recipient=user)
#             db.session.delete(subscription)
#             db.session.commit()
#             flash(gettext('"{}" has been unsubscribed from this ticket.'.format(user.name)), category='success')
#
#         else:
#
#             flash(gettext('Could not unsubscribe "{}" from ticket.'.format(user.name)), category='warning')
#
#         return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

# view to unsubscribe user from a ticket.
@flicket_bp.route(app.config['FLICKET'] + 'unsubscribe/<int:ticket_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def unsubscribe_ticket(ticket_id=None, user_id=None):
    if not ticket_id and user_id:
        return abort(404)

    form = UnSubscribeUser()

    ticket = FlicketTicket.query.filter_by(id=ticket_id).one()
    user = FlicketUser.query.filter_by(id=user_id).one()

    form.username.data = user.username

    if form.validate_on_submit():

        if ticket.can_unsubscribe(user):
            subscription = FlicketSubscription.query.filter_by(user=user, ticket=ticket).one()
            # unsubscribe user to ticket
            ticket.last_updated = datetime.datetime.now()
            add_action(ticket, 'unsubscribe', recipient=user)
            db.session.delete(subscription)
            db.session.commit()
            flash(gettext('"{}" has been unsubscribed from this ticket.'.format(user.name)), category='success')

        else:

            flash(gettext('Could not unsubscribe "{}" from ticket due to permission restrictions.'.format(user.name)),
                  category='warning')

        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    # else:
    #     print(form.errors)

    return render_template('flicket_unsubscribe_user.html', form=form, title='Unsubscribe', ticket=ticket, user=user)
