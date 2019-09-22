#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com


from application import db
from application.flicket.models.flicket_models import FlicketSubscription


def subscribe_user(ticket, user):
    if not ticket.is_subscribed(user):
        # subscribe user to ticket
        # noinspection PyArgumentList
        subscribe = FlicketSubscription(user=user, ticket=ticket)
        db.session.add(subscribe)
        db.session.commit()
        return True

    return False
