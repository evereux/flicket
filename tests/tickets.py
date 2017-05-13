#! usr/bin/python3
# -*- coding: utf-8 -*-

from flask import url_for

from setup import RunSetUP
from application import app
from application.flicket.models.flicket_models import FlicketPriority

from tests.main import TestCase, CreateUser, CreateDepartmentCategory, dump_to_tmp

class TestCaseTickets(TestCase):

    def test_create_ticket(self):

        with app.app_context():

            title = 'this is the title'
            content = 'this is some content'

            RunSetUP.create_default_priority_levels(silent=True)

            priority = FlicketPriority.query.first()

            create_category = CreateDepartmentCategory()
            user = CreateUser()

            self.login(username=user.username, password=user.password)

            _url = url_for('flicket_bp.ticket_create')
            result = self.client.post(_url, buffered=True, content_type='multipart/form-data',
                                      data={
                                          'title': title,
                                          'content': content,
                                          'priority': str(priority.id),
                                          'category': str(create_category.category_db.id),
                                          'file[]': ''
                                      }, follow_redirects=True)
            dump_to_tmp(result.data.decode(), 'create_ticket.html')

            self.logout()