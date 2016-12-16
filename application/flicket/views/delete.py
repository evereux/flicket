#! usr/bin/python3
# -*- coding: utf8 -*-

import os

from flask import flash, g, redirect, url_for, render_template
from flask_login import login_required

from application import app, db
from application.flicket.forms.forms_main import ConfirmPassword
from application.flicket.models.flicket_models import (FlicketTicket,
                                                       FlicketUploads,
                                                       FlicketPost,
                                                       FlicketCategory,
                                                       FlicketDepartment)
from . import flicket_bp


# delete ticket
@flicket_bp.route(app.config['FLICKET'] + 'delete_ticket/<ticket_id>', methods=['GET', 'POST'])
@login_required
def delete_ticket(ticket_id):
    # check is user is authorised to delete tickets. Currently, only admins can delete tickets.
    if not g.user.is_admin:
        flash('You are not authorised to delete tickets.', category='warning')
        return redirect(url_for('ticket_view', ticket_id=ticket_id))

    form = ConfirmPassword()

    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

    if form.validate_on_submit():

        # delete images from database and folder
        images = FlicketUploads.query.filter_by(topic_id=ticket_id)
        for i in images:
            # delete files
            os.remove(os.path.join(os.getcwd(), app.config['TICKET_UPLOAD_FOLDER'] + '/' + i.file_name))
            # remove from database
            db.session.delete(i)

        db.session.delete(ticket)
        # commit changes
        db.session.commit()
        flash('ticket deleted', category='success')
        return redirect(url_for('flicket_bp.tickets_main'))

    return render_template('flicket_deletetopic.html',
                           form=form,
                           ticket=ticket,
                           title='Flicket - Delete Ticket')


# delete post
@flicket_bp.route(app.config['FLICKET'] + 'delete_post/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    # check user is authorised to delete posts. Only admin can do this.
    if not g.user.is_admin:
        flash('You are not authorised to delete posts', category='warning')

    form = ConfirmPassword()

    post = FlicketPost.query.filter_by(id=post_id).first()

    if form.validate_on_submit():

        # delete images from database and folder
        images = FlicketUploads.query.filter_by(posts_id=post_id)
        for i in images:
            # delete files
            os.remove(os.path.join(os.getcwd(), app.config['TICKET_UPLOAD_FOLDER'] + '/' + i.file_name))
            # remove from database
            db.session.delete(i)

        db.session.delete(post)
        # commit changes
        db.session.commit()
        flash('ticket deleted', category='success')
        return redirect(url_for('flicket_bp.tickets_main'))

    return render_template('flicket_deletepost.html',
                           form=form,
                           post=post,
                           title='Flicket - Delete post')


# delete category
@flicket_bp.route(app.config['FLICKET'] + 'delete/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def delete_category(category_id=False):
    if category_id:

        # check user is authorised to delete categories. Only admin can do this.
        if not g.user.is_admin:
            flash('You are not authorised to delete categories.', category='warning')

        form = ConfirmPassword()

        categories = FlicketTicket.query.filter_by(category_id=category_id)
        category = FlicketCategory.query.filter_by(id=category_id).first()

        # stop the deletion of categories assigned to tickets.
        if categories.count() > 0:
            flash('Category is linked to posts. Category can not be deleted unless link is removed.', category="danger")
            return redirect(url_for('flicket_bp.departments'))

        if form.validate_on_submit():
            # delete category from database
            category = FlicketCategory.query.filter_by(id=category_id).first()

            db.session.delete(category)
            # commit changes
            db.session.commit()
            flash('Category deleted', category='success')
            return redirect(url_for('flicket_bp.departments'))

        notification = "You are trying to delete category <span class=\"label label-default\">{}</span> that belongs to department <span class=\"label label-default\">{}</span>.".format(
            category.category, category.department.department)

        return render_template('flicket_delete.html',
                               form=form,
                               notification=notification,
                               title='Flicket - Delete')


# delete department
@flicket_bp.route(app.config['FLICKET'] + 'delete/department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def delete_department(department_id=False):
    if department_id:

        # check user is authorised to delete departments. Only admin can do this.
        if not g.user.is_admin:
            flash('You are not authorised to delete departments.', category='warning')

        form = ConfirmPassword()

        #
        departments = FlicketCategory.query.filter_by(department_id=department_id)
        department = FlicketDepartment.query.filter_by(id=department_id).first()

        # we can't delete any departments associated with categories.
        if departments.count() > 0:
            flash(
                'Department has categories linked to it. Department can not be deleted unless the categories are removed.',
                category="danger")
            return redirect(url_for('departments'))

        if form.validate_on_submit():
            # delete category from database
            department = FlicketDepartment.query.filter_by(id=department_id).first()

            db.session.delete(department)
            # commit changes
            db.session.commit()
            flash('Department {} deleted.'.format(department.department), category='success')
            return redirect(url_for('departments'))

        notification = "You are trying to delete department <span class=\"label label-default\">{}</span>.".format(
            department.department)

        return render_template('flicket_delete.html',
                               form=form,
                               notification=notification,
                               title='Flicket - Delete')
