import datetime

from flask import redirect, url_for, flash, render_template, g, request
from flask_login import login_required

from application import app, db

from flicket_application.flicket_forms import CreateTicket, ContentForm
from flicket_application.flicket_models import FlicketTicket, FlicketUploads, FlicketPost
from flicket_application.flicket_upload import upload_documents, add_upload_to_db
from flicket_application.flicket_functions import is_ticket_closed

# edit ticket
@app.route(app.config['FLICKETHOME'] + 'edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):

    form = CreateTicket()

    ticket = FlicketTicket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Could not find ticket.', category='warning')
        return redirect(url_for('flicket_main'))

    # check to see if topic is closed. ticket can't be edited once it's closed.
    if is_ticket_closed(ticket.current_status.status, ticket.id):
        return redirect(url_for('ticket_view', ticket_id=ticket.id))

    # check user is authorised to edit ticket. Currently, only admin or author can do this.
    if (ticket.user != g.user) or (not g.user.is_admin):
        flash('You are not authorised to edit this ticket.', category='warning')
        return redirect(url_for('ticket_view', ticket_id=ticket_id))

    if form.validate_on_submit():

        ticket.content = form.content.data
        ticket.title = form.title.data
        ticket.modified = g.user
        ticket.date_modified = datetime.datetime.now()

        files = request.files.getlist("file[]")
        new_files = upload_documents(files)

        # add files to database.
        post_type = 'Ticket'
        add_upload_to_db(new_files, ticket, post_type)

        db.session.commit()
        flash('Ticket topic edited.', category='success')
        return redirect(url_for('ticket_view', ticket_id=ticket_id))

    form.title.data = ticket.title
    form.content.data = ticket.content
    form.priority.data = ticket.ticket_priority_id

    return render_template('flicket/flicket_edittopic.html',
                           title='Flicket - Edit Ticket',
                           form=form)


# edit post
@app.route(app.config['FLICKETHOME'] + 'edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    form = ContentForm()

    post = FlicketPost.query.filter_by(id=post_id).first()

    if not post:
        flash('Could not find post.', category='warning')
        return redirect(url_for('flicket_main'))

    # check to see if topic is closed. ticket can't be edited once it's closed.
    if is_ticket_closed(post.add_ticket.current_status.status, post.add_ticket.id):
        return redirect(url_for('ticket_view', ticket_id=post.add_ticket.id))

    # check user is authorised to edit post. Only author or admin can do this.
    if (post.user != g.user) or (not g.user.is_admin):
        flash('You are not authorised to edit this ticket.', category='warning')
        return redirect(url_for('ticket_view', ticket_id=post.ticket_id))

    if form.validate_on_submit():
        post.content = form.content.data
        post.modified = g.user
        post.date_modified = datetime.datetime.now()

        files = request.files.getlist("file[]")
        new_files = upload_documents(files)

        if new_files == False:
            flash('There was a problem uploading files.', category='danger')
            return redirect(url_for('tickets_main'))

        # add files to database.
        post_type = 'Post'
        add_upload_to_db(new_files, post, post_type)

        db.session.commit()
        flash('Flicket edited.', category='success')

        return redirect(url_for('ticket_view', ticket_id=post.ticket_id))

    form.content.data = post.content

    return render_template('flicket/flicket_editpost.html',
                           title='Flicket - Edit Post',
                           form=form)
