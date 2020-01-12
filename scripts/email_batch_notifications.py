#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import time

from flask_script import Command
from sqlalchemy import or_

from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.email import FlicketMail


class EmailOutStandingTickets(Command):
    """
    Script to be run independently of the webserver. Script emails users a list of outstanding tickets that they have
    created or been assigned. To be run on a regular basis using a cron job or similar.
    Email functionality has to be enabled.
    """

    def run(self):
        # find all users
        users = FlicketUser.query.all()
        for user in users:
            # that have created a ticket or have a ticket assigned to them.
            tickets = FlicketTicket.query.filter(or_(
                FlicketTicket.user == user,
                FlicketTicket.assigned == user,
            )).filter(
                FlicketTicket.status_id != 2)

            if tickets.count() > 0:
                mail = FlicketMail()
                mail.tickets_not_closed(user, tickets)
                time.sleep(10)
