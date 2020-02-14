#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import redirect, url_for, g, flash
from flask_babel import gettext
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus
from application.flicket.scripts.flicket_functions import add_action
from application.flicket.scripts.email import FlicketMail


# close ticket
@flicket_bp.route(app.config['FLICKET'] + 'change_status/<ticket_id>/<status>/', methods=['GET', 'POST'])
@login_required
def change_status(ticket_id, status):
    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()
    closed = FlicketStatus.query.filter_by(status=status).first()

    # Check to see if user is authorised to close ticket.
    edit = False
    if ticket.user == g.user:
        edit = True
    if ticket.assigned == g.user:
        edit = True
    if g.user.is_admin:
        edit = True

    if not edit:
        flash(gettext('Only the person to which the ticket has been assigned, creator or Admin can close this ticket.'),
              category='warning')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    # Check to see if the ticket is already closed.
    if ticket.current_status.status == 'Closed':
        flash(gettext('Ticket is already closed.'), category='warning')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    f_mail = FlicketMail()
    f_mail.close_ticket(ticket)

    # add action record
    add_action(ticket, 'close')

    ticket.current_status = closed
    ticket.assigned_id = None
    ticket.last_updated = datetime.datetime.now()
    db.session.commit()

    flash(gettext('Ticket %(value)s closed.', value=str(ticket_id).zfill(5)), category='success')

    return redirect(url_for('flicket_bp.tickets'))
