#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import os
import unittest

from application import app, db, lm
from application.flicket.models.flicket_user import FlicketUser, FlicketGroup
from application.flicket.scripts.hash_password import hash_password
from tests.base_dir import base_dir
from setup import TestingSetUp


def dump_to_tmp(contents, filename):
    """
    Function to dump the html response to a file so we can view it's contents.
    Usage: # dump_to_tmp(rv.data.decode(), 'test.html')
    :param contents: 
    :param filename: 
    :return: 
    """
    filename = os.path.join(base_dir, "tmp/{}".format(filename))

    with open(filename, 'w') as f:
        f.write(contents)


class TestUsers:

    def __init__(self):

        self.username = 'jdoe'
        self.name = 'john doe'
        self.password = '12345'
        self.password_hash = hash_password(password=self.password)
        self.email = 'email@testing.com'
        self.password_hash = hash_password(password=self.password)
        self.date_added = datetime.datetime.now()

    def create_user(self):

        user = FlicketUser(username=self.username, name=self.name, email=self.email, password=self.password_hash, date_added=self.date_added)
        db.session.add(user)
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

    def test_index(self):
        rv = self.client.get('/', follow_redirects=True)
        assert b'Flicket is a simple Flask driven ticket system.' in rv.data

    def test_login_logout(self):
        # create the test user
        test_user = TestUsers()
        test_user.create_user()
        # login
        rv = self.login(username=test_user.username, password=test_user.password)
        assert b'You were logged in successfully.' in rv.data
        # logout
        rv = self.logout()
        dump_to_tmp(rv.data.decode(), 'test.html')
        assert b'You were logged out successfully.' in rv.data
