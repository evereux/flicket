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
from application.flicket.scripts.flicket_functions import add_action
from application.flicket.scripts.email import FlicketMail


# view for self claim a ticket
@flicket_bp.route(app.config['FLICKET'] + 'ticket_claim/<int:ticket_id>/', methods=['GET', 'POST'])
@login_required
def ticket_claim(ticket_id=False):
    if ticket_id:
        # claim ticket
        ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

        if ticket.assigned == g.user:
            flash(gettext('You have already been assigned this ticket.'), category='success')
            return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

        # set status to in work
        status = FlicketStatus.query.filter_by(status='In Work').first()
        ticket.assigned = g.user
        g.user.total_assigned += 1
        ticket.current_status = status
        ticket.last_updated = datetime.datetime.now()
        db.session.commit()

        # add action record
        add_action(ticket, 'claim')

        # send email notifications
        f_mail = FlicketMail()
        f_mail.assign_ticket(ticket=ticket)

        flash(gettext('You claimed ticket: %(value)s', value=ticket.id))
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    return redirect(url_for('flicket_bp.tickets'))
