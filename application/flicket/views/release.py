#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import redirect, url_for, flash, g
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus
from application.flicket.scripts.flicket_functions import announcer_post


# view to release a ticket user has been assigned.
@flicket_bp.route(app.config['FLICKETHOME'] + 'release/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def release(ticket_id=False):
    if ticket_id:

        ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

        # is ticket assigned.
        if not ticket.assigned:
            flash('Ticket has not been assigned')
            return redirect(url_for('ticket_view', ticket_id=ticket_id))

        # check ticket is owned by user or user is admin
        if (ticket.assigned.id != g.user.id) and (not g.user.is_admin):
            flash('You can not release a ticket you are not working on.')
            return redirect(url_for('ticket_view', ticket_id=ticket_id))

        # set status to open
        status = FlicketStatus.query.filter_by(status='Open').first()
        ticket.current_status = status
        ticket.assigned = None
        db.session.commit()

        # add post to say user claimed ticket.
        announcer_post(ticket_id, g.user, 'Ticket unassigned by')

        flash('You released ticket: {}'.format(ticket.id))
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    return redirect(url_for('flicket_bp.tickets_main'))
