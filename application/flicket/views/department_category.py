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
from application.flicket.scripts.flicket_functions import add_action
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
                'Category "{} / {}" '
                'is already assigned to ticket.'.format(ticket.category.category, ticket.category.department.department)),
                category='warning')
            return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

        # change category
        ticket.category_id = department_category.category_id

        # add action record
        add_action(ticket, 'department_category', data={
            'department_category': department_category.department_category,
            'category_id': department_category.category_id,
            'category': department_category.category,
            'department_id': department_category.department_id,
            'department': department_category.department})

        db.session.commit()

        flash(gettext('You changed category of ticket: {}'.format(ticket_id)), category='success')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    title = gettext('Change Department / Category of Ticket')

    return render_template("flicket_department_category.html", title=title, form=form, ticket=ticket)
