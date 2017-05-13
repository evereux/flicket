#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import os
import unittest

from application import app, db, lm
from application.flicket.models.flicket_user import FlicketUser, FlicketGroup, flicket_groups
from application.flicket.scripts.hash_password import hash_password
from tests.base_dir import base_dir
from setup import TestingSetUp


def dump_to_tmp(contents, filename):
    """
    Function to dump the html response to a file so we can view it's contents.
    Usage: # dump_to_tmp(result.data.decode(), 'test.html')
    :param contents: 
    :param filename: 
    :return: 
    """
    filename = os.path.join(base_dir, "tmp/{}".format(filename))

    with open(filename, 'w') as f:
        f.write(contents)


class CreateUser:
    def __init__(self, username='jdoe', name='john doe', password='12345', email='email@testing.com'):
        self.username = username
        self.name = name
        self.password = password
        self.password_hash = hash_password(password=self.password)
        self.email = email
        self.password_hash = hash_password(password=self.password)
        self.date_added = datetime.datetime.now()

        user = FlicketUser(username=self.username, name=self.name, email=self.email, password=self.password_hash,
                           date_added=self.date_added)
        db.session.add(user)
        db.session.commit()


class CreateAdmin:
    def __init__(self, username='admin', name='admin', password='12345', email='admin@testing.com'):
        self.username = username
        self.name = name
        self.password = password
        self.password_hash = hash_password(password=self.password)
        self.email = email
        self.password_hash = hash_password(password=self.password)
        self.date_added = datetime.datetime.now()

        self.user = FlicketUser(username=self.username, name=self.name, email=self.email, password=self.password_hash,
                                date_added=self.date_added)
        db.session.add(self.user)

        group = FlicketGroup(group_name='flicket_admin')
        db.session.add(group)
        group.users.append(self.user)
        db.session.commit()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestConfiguration')
        lm.init_app(app)
        self.client = app.test_client()
        db.create_all()

        TestingSetUp.set_db_config_defaults_testing(silent=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username='', password=''):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)


class TestCase_Pages(TestCase):
    def test_login_logout(self):
        # create the test user
        test_user = CreateUser()
        # login
        result = self.login(username=test_user.username, password=test_user.password)
        assert b'You were logged in successfully.' in result.data
        # logout
        result = self.logout()
        assert b'You were logged out successfully.' in result.data

    def test_index(self):
        # make sure user is redirected if not logged in
        result = self.client.get('/')
        self.assertEqual(result.status_code, 302)

        # create test user
        test_user = CreateUser()
        self.login(username=test_user.username, password=test_user.password)

        # retry page
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Stats', result.data)
        self.logout()

    def test_tickets(self):
        result = self.client.get('/tickets/')
        self.assertEqual(result.status_code, 302)

        test_user = CreateUser()
        self.login(username=test_user.username, password=test_user.password)

        result = self.client.get('/tickets/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Tickets', result.data)
        self.logout()

    def test_create_ticket(self):
        result = self.client.get('/ticket_create/')
        self.assertEqual(result.status_code, 302)

        test_user = CreateUser()
        self.login(username=test_user.username, password=test_user.password)

        result = self.client.get('/ticket_create/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Create Ticket', result.data)
        self.logout()

    def test_departments(self):
        result = self.client.get('/departments/')
        self.assertEqual(result.status_code, 302)

        test_user = CreateUser()
        self.login(username=test_user.username, password=test_user.password)

        result = self.client.get('/departments/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Departments', result.data)
        self.logout()

    def test_users(self):
        result = self.client.get('/users/')
        self.assertEqual(result.status_code, 302)

        test_user = CreateUser()
        self.login(username=test_user.username, password=test_user.password)

        result = self.client.get('/users/')
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

    def test_admin(self):
        user = CreateUser()
        admin = CreateAdmin()
        self.admin_page_tests('/flicket_admin/', user=user, admin=admin)
        self.admin_page_tests('/flicket_admin/config/', user=user, admin=admin)
        self.admin_page_tests('/flicket_admin/users/', user=user, admin=admin)
        self.admin_page_tests('/flicket_admin/add_user/', user=user, admin=admin)
        self.admin_page_tests('/flicket_admin/edit_user/?id=1', user=user, admin=admin)
        self.admin_page_tests('/flicket_admin/groups/', user=user, admin=admin)
