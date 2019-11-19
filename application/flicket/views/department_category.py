#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort, redirect, url_for, flash, render_template, g
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.forms.flicket_forms import ChangeDepartmentCategoryForm
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_models import FlicketDepartmentCategory
from application.flicket.models.flicket_models import FlicketStatus
from application.flicket.models.flicket_models import FlicketSubscription
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_functions import add_action
from application.flicket.scripts.email import FlicketMail
from . import flicket_bp


# tickets main
@flicket_bp.route(app.config['FLICKET'] + 'ticket_department_category/<int:ticket_id>/', methods=['GET', 'POST'])
@login_required
def ticket_department_category(ticket_id=False):
    if not app.config['change_category']:
        abort(404)

    if app.config['change_category_only_admin_or_super_user']:
        if not g.user.is_admin and not g.user.is_super_user:
            abort(404)

    form = ChangeDepartmentCategoryForm()
    ticket = FlicketTicket.query.get_or_404(ticket_id)

    if ticket.current_status.status == 'Closed':
        flash(gettext("Can't change the department and category on a closed ticket."))
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    if form.validate_on_submit():
        department_category = FlicketDepartmentCategory.query.filter_by(
            department_category=form.department_category.data).one()

        if ticket.category_id == department_category.category_id:
            flash(gettext(
                f'Category "{ticket.category.category} / {ticket.category.department.department}" is already assigned to ticket.'),
                category='warning')
            return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

        # change category, unassign and set status to open
        status = FlicketStatus.query.filter_by(status='Open').one()
        ticket.category_id = department_category.category_id
        ticket.current_status = status
        if ticket.assigned:
            ticket.assigned.total_assigned -= 1
            ticket.assigned = None

        # add action record
        add_action(ticket, 'department_category', data={
            'department_category': department_category.department_category,
            'category_id': department_category.category_id,
            'category': department_category.category,
            'department_id': department_category.department_id,
            'department': department_category.department})
        add_action(ticket, 'status', data={'status_id': status.id, 'status': status.status})

        # subscribe to the ticket
        if not ticket.is_subscribed(g.user):
            subscribe = FlicketSubscription(
                ticket=ticket,
                user=g.user
            )
            db.session.add(subscribe)

        db.session.commit()

        # send email to state ticket has been assigned.
        f_mail = FlicketMail()
        f_mail.department_category_ticket(ticket)

        flash(gettext(f'You changed category of ticket: {ticket_id}'), category='success')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    title = gettext('Change Department / Category of Ticket')

    return render_template("flicket_department_category.html", title=title, form=form, ticket=ticket)
