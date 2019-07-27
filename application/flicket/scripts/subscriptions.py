#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash
from flask_babel import gettext

from flask import g

from application import db
from application.flicket.models.flicket_models import  FlicketTicket, FlicketSubscription


def subscribe_user(ticket, user):

    if not ticket.is_subscribed(user):
        # subscribe user to ticket
        subscribe = FlicketSubscription(user=user, ticket=ticket)
        db.session.add(subscribe)
        db.session.commit()
        return True

    return False