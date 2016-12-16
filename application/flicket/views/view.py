#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime

from flask import render_template, redirect, url_for, g, request, flash
from flask_login import login_required

from . import flicket_bp
from application import app, db
from application.flicket.forms.flicket_forms import ContentForm
from application.flicket.models.flicket_models import FlicketTicket, FlicketStatus, FlicketPost
from application.flicket.scripts.flicket_functions import block_quoter
from application.flicket.scripts.flicket_upload import upload_documents, add_upload_to_db


# view ticket details
@flicket_bp.route(app.config['FLICKET'] + 'ticket_view/<ticket_id>/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKET'] + 'ticket_view/<ticket_id>/<int:page>/', methods=['GET', 'POST'])
@login_required
def ticket_view(ticket_id, page=1):

    # is ticket number legitimate
    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Cannot find ticket: "{}"'.format(ticket_id), category='warning')
        return redirect(url_for('flicket_bp.tickets_main'))

    # find all replies to ticket.
    replies = FlicketPost.query.filter_by(ticket_id=ticket_id).order_by(FlicketPost.date_added.asc())

    post_id = request.args.get('post_id')
    ticket_rid = request.args.get('ticket_rid')

    form = ContentForm()

    # add reply post
    if form.validate_on_submit():

        # upload file if user has selected one and the file is in accepted list of
        files = request.files.getlist("file[]")

        new_files = upload_documents(files)

        if new_files == False:
            flash('There was a problem uploading files for your post.', category='danger')
            return redirect(url_for('flicket_bp.tickets_main'))

        new_reply = FlicketPost(
            ticket=ticket,
            user=g.user,
            date_added=datetime.datetime.now(),
            content=form.content.data
        )

        # add documents to database
        post_type = 'Post'
        add_upload_to_db(new_files, new_reply, post_type)

        db.session.add(new_reply)

        open = FlicketStatus.query.filter_by(status='Open').first()
        ticket.current_status = open
        db.session.commit()

        return redirect(url_for('flicket_bp.ticket_view', ticket_id=ticket_id))

    if request.method == 'POST':
        if request.form['close-ticket'] == 'close':
            ticket_status = FlicketStatus.query.filter_by(status='closed').first()
            ticket.current_status = ticket_status
            db.session.commit()
            flash('Ticket closed!')

            return redirect(url_for('flicket_bp.tickets_main'))

    # get post id and populate contents for auto quoting
    if post_id:
        query = FlicketPost.query.filter_by(id=post_id).first()
        reply_contents = "{} wrote on {}\r\n\r\n{}".format(query.user.name, query.date_added, query.content)
        form.content.data = block_quoter(reply_contents)
    if ticket_rid:
        reply_contents = "{} wrote on {}\r\n\r\n{}".format(ticket.user.name, ticket.date_added, ticket.content)
        form.content.data = block_quoter(reply_contents)

    replies = replies.paginate(page, app.config['POSTS_PER_PAGE'])

    return render_template('flicket_view.html',
                           title='Flicket - View Ticket',
                           ticket=ticket,
                           form=form,
                           replies=replies,
                           post_id=post_id,
                           page=page)
