#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime
import json
import os

from flask_script import Command

from scripts.users_export_to_json import json_user_file
from application import db
from application.flicket.models.flicket_user import FlicketUser


class JsonUser:

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.name = name
        self.password = password


class ImportUsersFromJson(Command):
    """
    Command used by manage.py to import users from a json file formatted such:
        [
            { username, name, email, password.
        ]
    """

    @staticmethod
    def run():

        # check if file exists
        if not os.path.isfile(json_user_file):
            print('Could not find json file "{}". Exiting ....'.format(json_user_file))
            exit()

        # read json file
        with open(json_user_file) as data_file:
            json_users = json.load(data_file)

        # check formatting of json file
        valid_json_fields = ['username', 'name', 'email', 'password']
        for user in json_users:
            if not all(f in user for f in valid_json_fields):
                print('json file not formatted correctly. Exiting.')
                exit()

        # add users to database.
        for user in json_users:

            # encode password to bytes
            password = str.encode(user['password'])

            # create json_user object
            json_user = JsonUser(user['username'], user['name'], user['email'], password)

            # check tht user doesn't already exist.
            existing_user = FlicketUser.query.filter_by(email=json_user.email)
            if existing_user.count() > 0:
                print('User {} {} already exists in the database.'.format(json_user.name, json_user.email))
                continue

            # add the user
            print('Adding the user {} {} to the database.'.format(json_user.name, json_user.email))
            new_user = FlicketUser(username=json_user.username, name=json_user.name, email=json_user.email,
                                   password=json_user.password, date_added=datetime.datetime.now())
            db.session.add(new_user)
            db.session.commit()
