#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import url_for

from application.flicket.models.flicket_models import FlicketTicket, FlicketPost


def generate_choices(item, id=id):

    query = None

    if item == 'Ticket':
        query = FlicketTicket.query.filter_by(id=id).first()
    elif item == 'Post':
        query = FlicketPost.query.filter_by(id=id).first()

    if query:

        # define the multi select box for document uploads
        upload = []
        for u in query.uploads:
            upload.append((u.id, u.filename, u.original_filename))

        uploads = []

        for x in upload:
            uri = url_for('flicket_bp.view_ticket_uploads', filename=x[1])
            uri_label = '<a href="' + uri + '">' + x[2] + '</a>'
            uploads.append((x[0], uri_label))

        return uploads
