#! usr/bin/python3
# -*- coding: utf-8 -*-

from flask import url_for

from application import app
from .main import TestCase, CreateUser, CreateAdmin

class TestCasePages(TestCase):

    def test_login_logout(self):
        # create the test user
        test_user = CreateUser()
        # login
        result = self.login(username=test_user.username, password=test_user.password)
        assert b'You were logged in successfully.' in result.data
        # logout
        result = self.logout()
        assert b'You were logged out successfully.' in result.data

    def test_page_index(self):

        with app.app_context():

            _url = url_for('flicket_bp.index')
            # make sure user is redirected if not logged in
            result = self.client.get(_url)
            self.assertEqual(result.status_code, 302)

            # create test user
            test_user = CreateUser()
            self.login(username=test_user.username, password=test_user.password)

            # retry page
            result = self.client.get(_url)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Stats', result.data)
            self.logout()

    def test_page_tickets(self):

        with app.app_context():

            _url = url_for('flicket_bp.tickets')

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 302)

            test_user = CreateUser()
            self.login(username=test_user.username, password=test_user.password)

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Tickets', result.data)
            self.logout()

    def test_page_create_ticket(self):

        with app.app_context():

            _url = url_for('flicket_bp.ticket_create')

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 302)

            test_user = CreateUser()
            self.login(username=test_user.username, password=test_user.password)

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Create Ticket', result.data)
            self.logout()

    def test_page_departments(self):

        with app.app_context():

            _url = url_for('flicket_bp.departments')

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 302)

            test_user = CreateUser()
            self.login(username=test_user.username, password=test_user.password)

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Departments', result.data)
            self.logout()

    def test_page_users(self):

        with app.app_context():

            _url = url_for('flicket_bp.flicket_users')

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 302)

            test_user = CreateUser()
            self.login(username=test_user.username, password=test_user.password)

            result = self.client.get(_url)
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'Users', result.data)
            self.logout()

    def admin_page_tests(self, url, user=None, admin=None):
        """
        Admin pages should return 302 for non logged in user, 403 for logged in non admin 
        add 200 for logged in user.
        :return:
        """

        result = self.client.get(url)
        self.assertEqual(result.status_code, 302)

        self.login(username=user.username, password=user.password)
        result = self.client.get(url)
        self.assertEqual(result.status_code, 403)
        self.logout()

        self.login(username=admin.username, password=admin.password)
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)
        self.logout()

    def test_pages_admin(self):

        with app.app_context():
            user = CreateUser()
            admin = CreateAdmin()
            self.admin_page_tests(url_for('admin_bp.index'), user=user, admin=admin)
            self.admin_page_tests(url_for('admin_bp.config'), user=user, admin=admin)
            self.admin_page_tests(url_for('admin_bp.users'), user=user, admin=admin)
            self.admin_page_tests(url_for('admin_bp.add_user'), user=user, admin=admin)
            self.admin_page_tests(url_for('admin_bp.edit_user', id=1), user=user, admin=admin)
            self.admin_page_tests(url_for('admin_bp.groups'), user=user, admin=admin)
