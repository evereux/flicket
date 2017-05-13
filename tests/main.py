#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime
import os
import unittest

from application import app, db, lm
from application.flicket.models.flicket_user import FlicketUser, FlicketGroup
from application.flicket.models.flicket_models import FlicketCategory, FlicketDepartment, FlicketPriority
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

class CreateDepartmentCategory:
    def __init__(self, department='IT', category='Morons'):

        self.department = department
        self.category = category

        self.department_db = FlicketDepartment(department=self.department)
        db.session.add(self.department_db)
        self.category_db = FlicketCategory(category=self.category, department=self.department_db)
        db.session.add(self.category_db)
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




