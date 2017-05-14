#! usr/bin/python3
# -*- coding: utf-8 -*-

from flask import url_for

from application import app
from application.flicket.models.flicket_models import FlicketPriority, FlicketCategory
from application.flicket.models.flicket_user import FlicketUser

from tests.main import TestCase, CreateUser, dump_to_tmp, CreateTicket

class TestCaseTickets(TestCase):

    def test_create_ticket(self):

        with app.app_context():

            title = 'this is the title'
            content = 'this is some content'

            # get data for forms submission
            priority = FlicketPriority.query.first()
            category = FlicketCategory.query.first()

            user = CreateUser()

            self.login(username=user.username, password=user.password)
            _url = url_for('flicket_bp.ticket_create')

            result = self.client.post(_url, buffered=True, content_type='multipart/form-data',
                                      data={
                                          'title': title,
                                          'content': content,
                                          'priority': str(priority.id),
                                          'category': str(category.id),
                                          'file[]': '',
                                          'submit': 'Submit'
                                      }, follow_redirects=True)

            self.assertIn(b'new ticket created', result.data.lower())
            self.logout()

    def test_create_reply_and_quote(self):

        with app.app_context():

            user = CreateUser()
            ticket = CreateTicket(user.user)

            _url = url_for('flicket_bp.ticket_view', page=1, ticket_id=ticket.ticket.id, ticket_rid=ticket.ticket.id)
            result = self.client.get(_url, follow_redirects=True)

            self.assertEqual(result.status_code, 200)
