#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import redirect, url_for, g, flash
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus
from application.flicket.scripts.flicket_functions import notification_post


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
        flash('Only the person to which the ticket has been assigned, creator or Admin can close this ticket.',
              category='warning')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    # Check to see if the ticket is already closed.
    if ticket.current_status.status == 'Closed':
        flash('Ticket is already closed.', category='warning')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    notification_post(ticket_id, g.user, 'Ticket closed by')
    ticket.current_status = closed
    ticket.assigned_id = None
    db.session.commit()

    flash('Ticket {} closed.'.format(str(ticket_id).zfill(5)), category='success')

    return redirect(url_for('flicket_bp.tickets_main'))
