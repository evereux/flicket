#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import time

from flask_script import Command

from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.email import FlicketMail


class EmailOutStandingTickets(Command):

    def run(self):
        # find all users
        users = FlicketUser.query.all()
        for user in users:
            # that have created a ticket or have a ticket assigned to them.
            tickets = FlicketTicket.query.filter(
                FlicketTicket.user == user).filter(
                FlicketTicket.assigned == user).filter(
                FlicketTicket.status_id != 2).all()

            mail = FlicketMail()
            mail.tickets_not_closed(user, tickets)
            time.sleep(10)
