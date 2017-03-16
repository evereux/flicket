#! usr/bin/python3
# -*- coding: utf8 -*-


import json
import os

from scripts.create_json import WriteConfigJson, config_file

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfiguration(object):

    WriteConfigJson().json_exists()

    # get data from config file
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    DEBUG = False
    TESTING = False
    EXPLAIN_TEMPLATE_LOADING = False

    # user login information for database user.
    db_username = config_data['db_username']
    db_password = config_data['db_password']
    # database connection details
    db_url = config_data['db_url']
    db_port = config_data['db_port']
    db_name = config_data['db_name']
    db_type = 'mysql+pymysql'

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(db_type,
                                                           db_username,
                                                           db_password,
                                                           db_url,
                                                           db_port,
                                                           db_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # default flicket_admin group name
    ADMIN_GROUP_NAME = 'flicket_admin'

    SECRET_KEY = 'lkliaeo239jfj'

    # The base url for your application.
    WEBHOME = '/'
    # The base url for flicket.
    FLICKET = WEBHOME + ''
    FLICKET_API = WEBHOME + 'flicket-api/'
    ADMINHOME = '/flicket_admin/'

    ANNOUNCER = {'name': 'announcer',
                 'username': 'announcer',
                 'password': 'm3r4nd0mstr1ng',
                 'email': 'flicket_admin@localhost.com'}


class TestConfiguration(BaseConfiguration):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    TESTING = True
    SESSION_PROTECTION = None
    LOGIN_DISABLED = True
