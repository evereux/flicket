#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import redirect, url_for, flash, g, render_template
from flask_login import login_required

from application import app, db
from application.flicket.forms.flicket_forms import SearchUserForm
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus, FlicketSubscription
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_functions import add_action
from application.flicket.scripts.email import FlicketMail
from . import flicket_bp


# tickets main
@flicket_bp.route(app.config['FLICKET'] + 'ticket_assign/<int:ticket_id>/', methods=['GET', 'POST'])
@login_required
def ticket_assign(ticket_id=False):
    form = SearchUserForm()
    ticket = FlicketTicket.query.filter_by(id=ticket_id).one()

    if ticket.current_status.status == 'Closed':
        flash("Can't assign a closed ticket.")
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    if form.validate_on_submit():

        user = FlicketUser.query.filter_by(username=form.username.data).first()

        if ticket.assigned == user:
            flash('User is already assigned to ticket.')
            return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

        # set status to in work
        status = FlicketStatus.query.filter_by(status='In Work').first()
        # assign ticket
        ticket.assigned = user
        ticket.current_status = status

        # add action record
        add_action(action='assign', ticket=ticket, recipient=user)

        # subscribe to the ticket
        if not ticket.is_subscribed(user):
            subscribe = FlicketSubscription(
                ticket=ticket,
                user=user
            )
            db.session.add(subscribe)

        db.session.commit()

        # send email to state ticket has been assigned.
        f_mail = FlicketMail()
        f_mail.assign_ticket(ticket)

        flash('You reassigned ticket:{}'.format(ticket.id))
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    return render_template("flicket_assign.html", title="Assign Ticket", form=form, ticket=ticket)
