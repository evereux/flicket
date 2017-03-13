#! usr/bin/python3
# -*- coding: utf8 -*-
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
from flask_mail import Message

from . import flicket_bp
from application import app, db, mail
from application.flicket.forms.flicket_forms import CreateTicketForm
from application.flicket.scripts.email import FlicketMail
from application.flicket.models.flicket_models import (FlicketTicket,
                                                       FlicketStatus,
                                                       FlicketPriority,
                                                       FlicketCategory)
from application.flicket.scripts.flicket_upload import upload_documents, add_upload_to_db


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

        new_files = upload_documents(files)

        if new_files is False:
            flash('There was a problem uploading files.', category='danger')
            return redirect(url_for('flicket_bp.tickets_main'))

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

        # add files to database.
        if new_files is not None:
            post_type = 'Ticket'
            add_upload_to_db(new_files, new_ticket, post_type)

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
