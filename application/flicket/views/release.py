#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import redirect, url_for, flash, g
from flask_babel import gettext
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus
from application.flicket.scripts.email import FlicketMail
from application.flicket.scripts.flicket_functions import add_action


# view to release a ticket user has been assigned.
@flicket_bp.route(app.config['FLICKET'] + 'release/<int:ticket_id>/', methods=['GET', 'POST'])
@login_required
def release(ticket_id=False):

    if ticket_id:

        ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

        # is ticket assigned.
        if not ticket.assigned:
            flash(gettext('Ticket has not been assigned'), category='warning')
            return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

        # check ticket is owned by user or user is admin
        if (ticket.assigned.id != g.user.id) and (not g.user.is_admin):
            flash(gettext('You can not release a ticket you are not working on.'), category='warning')
            return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

        # set status to open
        status = FlicketStatus.query.filter_by(status='Open').first()
        ticket.current_status = status
        ticket.last_updated = datetime.datetime.now()
        user = ticket.assigned
        ticket.assigned = None
        user.total_assigned -= 1

        db.session.commit()

        # add action record
        add_action(ticket, 'release')

        # send email to state ticket has been released.
        f_mail = FlicketMail()
        f_mail.release_ticket(ticket)

        flash(gettext('You released ticket: %(value)s', value=ticket.id), category='success')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    return redirect(url_for('flicket_bp.tickets'))
