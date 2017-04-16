#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import (flash,
                   redirect,
                   url_for,
                   request,
                   render_template,
                   g)
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import CreateTicketForm
from application.flicket.scripts.email import FlicketMail
from application.flicket.models.flicket_models import (FlicketTicket,
                                                       FlicketStatus,
                                                       FlicketPriority,
                                                       FlicketCategory)
from application.flicket.scripts.flicket_upload import UploadAttachment


# create ticket
@flicket_bp.route(app.config['FLICKET'] + 'ticket_create/', methods=['GET', 'POST'])
@login_required
def ticket_create():
    form = CreateTicketForm()

    if form.validate_on_submit():

        # this is a new post so ticket status is 'open'
        ticket_status = FlicketStatus.query.filter_by(status='open').first()
        ticket_priority = FlicketPriority.query.filter_by(id=int(form.priority.data)).first()
        ticket_category = FlicketCategory.query.filter_by(id=int(form.category.data)).first()

        files = request.files.getlist("file")
        upload_attachments = UploadAttachment(files)
        if upload_attachments.are_attachements():
            upload_attachments.upload_files()


        # submit ticket data to database
        new_ticket = FlicketTicket(title=form.title.data,
                                   date_added=datetime.datetime.now(),
                                   user=g.user,
                                   current_status=ticket_status,
                                   content=form.content.data,
                                   ticket_priority=ticket_priority,
                                   category=ticket_category
                                   )
        db.session.add(new_ticket)

        # add attachments to the dataabase.
        upload_attachments.populate_db(new_ticket)

        # commit changes to the database
        db.session.commit()

        # send email notification
        f_mail = FlicketMail()
        f_mail.create_ticket(ticket=new_ticket)

        flash('New Ticket created.', category='success')
        return redirect(url_for('flicket_bp.ticket_view', ticket_id=new_ticket.id))

    return render_template('flicket_create.html',
                           title='Flicket - Create Ticket',
                           form=form)
