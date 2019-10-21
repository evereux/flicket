#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import flash, g

from application import db
from application.flicket.models.flicket_models import FlicketAction


def add_action(ticket, action, data=None, recipient=None):
    """
    :param ticket: ticket object 
    :param action: string
    :param data: dictionary
    :param recipient: user object
    :return:
    """
    post_id = None
    if ticket.posts:
        post_id = ticket.posts[-1].id

    new_action = FlicketAction(
        ticket=ticket,
        post_id=post_id,
        action=action,
        data=data,
        user=g.user,
        recipient=recipient,
        date=datetime.datetime.now()
    )
    db.session.add(new_action)
    db.session.commit()


def is_ticket_closed(status):
    # check to see if topic is closed. ticket can't be edited once it's closed.
    if status == 'Closed':
        flash('Users can not edit closed tickets.', category='danger')
        return True


def block_quoter(foo):
    """
    Indents input with '> '. Used for quoting text in posts.
    :param foo:
    :return:
    """

    foo = foo.strip()
    split_string = foo.split('\n')
    new_string = ''
    if len(split_string) > 0:
        for i in split_string:
            temp_string = '> ' + i
            new_string += temp_string
        return new_string
    else:
        return '> ' + foo
