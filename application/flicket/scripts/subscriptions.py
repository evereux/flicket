#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com


from application import db
from application.flicket.models.flicket_models import FlicketSubscription
from application.flicket.scripts.flicket_functions import add_action


def subscribe_user(ticket, user):
    if not ticket.is_subscribed(user):
        # subscribe user to ticket
        # noinspection PyArgumentList
        subscribe = FlicketSubscription(user=user, ticket=ticket)
        add_action(ticket, 'subscribe', recipient=user)
        db.session.add(subscribe)
        db.session.commit()
        return True

    return False
