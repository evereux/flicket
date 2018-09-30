#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import os

from flask import redirect, url_for, flash, render_template, g, request
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import EditTicketForm, EditReplyForm
from application.flicket.models.flicket_models import (FlicketCategory,
                                                       FlicketHistory,
                                                       FlicketTicket,
                                                       FlicketPost,
                                                       FlicketPriority,
                                                       FlicketStatus,
                                                       FlicketUploads)
from application.flicket.scripts.flicket_functions import is_ticket_closed
from application.flicket.scripts.flicket_upload import UploadAttachment


# edit ticket
@flicket_bp.route(app.config['FLICKET'] + 'edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    form = EditTicketForm(ticket_id=ticket_id)

    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Could not find ticket.', category='warning')
        return redirect(url_for('flicket_bp.flicket_main'))

    # check to see if topic is closed. ticket can't be edited once it's closed.
    if is_ticket_closed(ticket.current_status.status):
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket.id))

    # check user is authorised to edit ticket. Currently, only admin or author can do this.
    not_authorised = True
    if ticket.user == g.user or g.user.is_admin:
        not_authorised = False

    if not_authorised:
        flash('You are not authorised to edit this ticket.', category='warning')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    if form.validate_on_submit():

        # before we make any changes store the original post content in the history table if it has changed.
        if ticket.modified_id:
            history_id = ticket.modified_id
        else:
            history_id = ticket.started_id
        if ticket.content != form.content.data:
            history = FlicketHistory(
                original_content=ticket.content,
                topic=ticket,
                date_modified=datetime.datetime.now(),
                user_id=history_id
            )
            db.session.add(history)

        # loop through the selected uploads for deletion.
        if len(form.uploads.data) > 0:
            for i in form.uploads.data:
                # get the upload document information from the database.
                query = FlicketUploads.query.filter_by(id=i).first()
                # define the full uploaded filename
                the_file = os.path.join(app.config['ticket_upload_folder'], query.filename)

                if os.path.isfile(the_file):
                    # delete the file from the folder
                    os.remove(the_file)

                db.session.delete(query)

        ticket_priority = FlicketPriority.query.filter_by(id=int(form.priority.data)).first()
        ticket_category = FlicketCategory.query.filter_by(id=int(form.category.data)).first()

        ticket.content = form.content.data
        ticket.title = form.title.data
        ticket.modified = g.user
        ticket.date_modified = datetime.datetime.now()
        ticket.status_id = form.status.data
        ticket.ticket_priority = ticket_priority
        ticket.category = ticket_category

        files = request.files.getlist("file")
        upload_attachments = UploadAttachment(files)
        if upload_attachments.are_attachements():
            upload_attachments.upload_files()

        # add files to database.
        upload_attachments.populate_db(ticket)

        db.session.commit()
        flash('Ticket successfully edited.', category='success')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    form.content.data = ticket.content
    form.priority.data = ticket.ticket_priority_id
    form.title.data = ticket.title
    form.category.data = ticket.category_id

    return render_template('flicket_edittopic.html',
                           title='Flicket - Edit Ticket',
                           form=form)


# edit post
@flicket_bp.route(app.config['FLICKET'] + 'edit_post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = EditReplyForm(post_id=post_id)

    post = FlicketPost.query.filter_by(id=post_id).first()

    if not post:
        flash('Could not find post.', category='warning')
        return redirect(url_for('flicket_bp.flicket_main'))

    # check to see if topic is closed. ticket can't be edited once it's closed.
    if is_ticket_closed(post.ticket.current_status.status):
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=post.ticket.id))

    # check user is authorised to edit post. Only author or admin can do this.
    not_authorised = True
    if post.user == g.user or g.user.is_admin:
        not_authorised = False
    if not_authorised:
        flash('You are not authorised to edit this ticket.', category='warning')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=post.ticket_id))

    if form.validate_on_submit():

        # stop closing of ticket via edit.
        if form.status.data == 2:
            flash('You can not edit and close ticket.')

        # before we make any changes store the original post content in the history table if it has changed.
        if post.modified_id:
            history_id = post.modified_id
        else:
            history_id = post.user_id
        if post.content != form.content.data:
            history = FlicketHistory(
                original_content=post.content,
                post=post,
                date_modified=datetime.datetime.now(),
                user_id=history_id
            )
            db.session.add(history)

        # loop through the selected uploads for deletion.
        if len(form.uploads.data) > 0:
            for i in form.uploads.data:
                # get the upload document information from the database.
                query = FlicketUploads.query.filter_by(id=i).first()
                # define the full uploaded filename
                the_file = os.path.join(app.config['ticket_upload_folder'], query.filename)

                if os.path.isfile(the_file):
                    # delete the file from the folder
                    os.remove(the_file)

                db.session.delete(query)

        post.content = form.content.data
        post.modified = g.user
        post.date_modified = datetime.datetime.now()

        post.ticket.status_id = form.status.data

        files = request.files.getlist("file")
        upload_attachments = UploadAttachment(files)
        if upload_attachments.are_attachements():
            upload_attachments.upload_files()

        # add files to database.
        upload_attachments.populate_db(post)

        db.session.commit()
        flash('Post successfully edited.', category='success')

        return redirect(url_for('flicket_bp.ticket_view', ticket_id=post.ticket_id))

    form.content.data = post.content

    return render_template('flicket_editpost.html',
                           title='Flicket - Edit Post',
                           form=form)
