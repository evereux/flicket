#! usr/bin/python3
# -*- coding: utf8 -*-

"""
testing module. lots of work to do here yet ...
"""

import datetime
import os
import unittest
from io import BytesIO

from coverage import coverage

from setup import create_admin, create_default_priority_levels, create_default_depts, create_admin_group, \
    for_testing_only

from application import app, db, lm
from application.flicket.scripts.hash_password import hash_password
from application.admin.models.user import User

basedir = os.path.abspath(os.path.dirname(__file__))


def dump_to_tmp(contents, filename):
    filename = os.path.join(basedir, "tmp/{}".format(filename))

    with  open(filename, 'w') as f:
        f.write(contents)


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestConfiguration')
        lm.init_app(app)
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username='', password=''):
        return self.client.post('/login', data=dict(
            username=username,
            password=password,
            file=''
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def populate_db_skeleton(self):
        """ Populate the database with defaults defined in setup.py """
        create_admin(username='admin', password='admin', email='admin@localhost.com', silent=True)
        create_admin_group(silent=True)
        create_default_priority_levels(silent=True)
        create_default_depts(silent=True)
        for_testing_only(silent=True)
        db.session.commit()

    def create_user(self, username='john_1234', email='good@email.com', password='12345'):
        # create a new user
        password = hash_password(password)
        _user = User(
            username=username,
            name=username,
            password=password,
            email=email,
            date_added=datetime.datetime.now()
        )
        db.session.add(_user)
        db.session.commit()
        return _user

    def add_ticket(self, title, content, priority='1', category='1', file=list):
        return self.client.post('flicket/ticket_create/', buffered=True,
                                content_type='multipart/form-data',
                                data={
                                    'title': title,
                                    'content': content,
                                    'priority': priority,
                                    'category': category,
                                    'file[]': file
                                }, follow_redirects=True)

    ####################################################################################################################
    ### TESTS ###

    def test_index(self):
        rv = self.client.get('/', follow_redirects=True)
        assert b'holding page' in rv.data

    def test_admin(self):
        with self.client as tc:
            self.populate_db_skeleton()

            # admin view requires admin login.
            rv = self.login(username='admin', password='admin')

            # load admin page
            rv = self.client.get('admin/', follow_redirects=True)
            assert b'Administration' in rv.data

            # test already logged in user.
            self.populate_db_skeleton()
            rv = self.login(username='paul', password='12345')
            rv = self.client.get('admin/', follow_redirects=True)
            assert b'Flicket is a simple Flask driven ticket system.' not in rv.data

            self.logout()
            rv = self.login(username='admin', password='admin')
            rv = self.client.get('admin/', follow_redirects=True)
            assert b'Administration' in rv.data

            rv = self.client.get('admin/admin_users/', follow_redirects=True)
            assert b'Click on username to edit.' in rv.data

            rv = self.client.get('admin/add_user/')
            assert b'Please add new users details.' in rv.data

            rv = self.client.post('admin/add_user/',
                                data={
                                    'username': 'lalala',
                                    'email': 'lala@lala.com',
                                    'name': 'lala lalala',
                                    'password': 'aaaAAA',
                                    'confirm': 'aaaAAA'
                                }, follow_redirects=True)
            dump_to_tmp(rv.data.decode(), 'dump.html')
            assert b'You have successfully registered new user' in rv.data

    def test_flicket_index(self):
        """ Test the loading of the flicket home page. """
        self.populate_db_skeleton()

        # Test the main page
        rv = self.client.get('flicket/', follow_redirects=True)
        assert b'Flicket is a simple Flask driven ticket system.' in rv.data

    def test_login_logout(self):
        """ Test that the login and logout views work as expected. """
        self.populate_db_skeleton()

        rv = self.login(username='admin', password='admin')

        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data

    def test_flicket_main(self):
        """ Test the loading of the flicket home page. """

        with self.client:
            self.populate_db_skeleton()

            rv = self.client.get('flicket/tickets_main/', follow_redirects=True)
            assert b'Flicket - Tickets' in rv.data

            # Test page with form search
            rv = self.client.post('flicket/tickets_main/?status=Open&category=PC&department=IT',
                                  data={
                                      'email': 'admin@localhost.com',
                                      'content': 'nipples'
                                  }, follow_redirects=True)

            assert b'Flicket - Tickets' in rv.data

    def test_flicket_creation(self):
        """ Tests the creation of tickets. """

        with self.client as tc:
            self.populate_db_skeleton()

            # create ticket view requires login.
            rv = self.login(username='admin', password='admin')

            # load the create ticket page
            rv = self.client.get('flicket/ticket_create/', follow_redirects=True)
            assert b'Create Ticket' in rv.data

            # define ticket contents
            title = 'some random title'
            content = 'some random ceontent'
            file = [(BytesIO(b'hello there'), 'hello.txt')]

            # add ticket with a file.
            rv = self.add_ticket(title, content, file=file)
            assert b'New Ticket created.' in rv.data
            # add ticket without a file
            file = []
            rv = self.add_ticket(title, content, file=file)
            assert b'New Ticket created.' in rv.data


# todo: add user to admin group

# todo: create topic

# todo: create topic with image

# todo: add reply to topic

# todo: add reply with image

# todo: edit topic

# todo: edit reply

# todo: delete topic

# todo: delete reply

# todo: can user edit other user posts

# todo: can user delete other user posts


if __name__ == '__main__':

    cov = coverage(branch=True, omit=['flask/*', 'tests.py', 'env-linux/*'])
    cov.start()
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print('\n\nCoverage Report:\n')
    cov.report()
    print("\nHTML version: {}".format(os.path.join(basedir, "tmp/coverage/index.html")))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
