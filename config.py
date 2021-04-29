#! usr/bin/python3
# -*- coding: utf8 -*-


import json
import os
import platform

from scripts.create_json import config_file
from scripts.create_json import WriteConfigJson
from scripts.create_json import check_db_connection

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):

    WriteConfigJson.json_exists()

    DEBUG = False
    TESTING = False
    EXPLAIN_TEMPLATE_LOADING = False

    try:

        # get data from config file
        with open(config_file, 'r') as f:
            config_data = json.load(f)

        # user login information for database user.
        db_username = config_data['db_username']
        db_password = config_data['db_password']
        # database connection details
        db_url = config_data['db_url']
        db_port = config_data['db_port']
        db_name = config_data['db_name']
        db_type = config_data['db_type']
        db_driver = config_data['db_driver']

    except KeyError:
        raise KeyError('The file config.json appears to incorrectly formatted.')

    db_dialect = None
    SQLALCHEMY_DATABASE_URI = None

    sql_os_path_prefix = '////'
    if platform.system() == 'Windows':
        sql_os_path_prefix = '///'

    if db_type == 1:
        db_dialect = 'sqlite'
        db_path = os.path.join(basedir, db_name)
        SQLALCHEMY_DATABASE_URI = f'{db_dialect}:{sql_os_path_prefix}{db_path}'

    else:

        if db_type == 2:
            db_dialect = 'postgresql'
        if db_type == 3:
            db_dialect = 'mysql'

        SQLALCHEMY_DATABASE_URI = f'{db_dialect}+{db_driver}://{db_username}:{db_password}@{db_url}:{db_port}/{db_name}'

    if SQLALCHEMY_DATABASE_URI is None:
        raise ConnectionAbortedError('Incorrect database type defined in config.json.')

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # default flicket_admin group name
    ADMIN_GROUP_NAME = 'flicket_admin'
    SUPER_USER_GROUP_NAME = 'super_user'

    SECRET_KEY = config_data['SECRET_KEY']

    # The base url for your application.
    WEBHOME = '/'
    # The base url for flicket.
    FLICKET = WEBHOME + ''
    FLICKET_API = WEBHOME + 'flicket-api/'
    FLICKET_REST_API = WEBHOME + 'flicket-rest-api'
    ADMINHOME = '/flicket_admin/'

    # flicket user used to post replies to tickets for status changes.
    NOTIFICATION = {'name': 'notification',
                    'username': 'notification',
                    'password': config_data['NOTIFICATION_USER_PASSWORD'],
                    'email': 'admin@localhost'}

    SUPPORTED_LANGUAGES = {'en': 'English', 'fr': 'Francais'}
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

    check_db_connection(SQLALCHEMY_DATABASE_URI)


class TestConfiguration(BaseConfiguration):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False
    TESTING = True
    SESSION_PROTECTION = None
    LOGIN_DISABLED = False
    SERVER_NAME = 'localhost:5001'
    config_data = {"db_username": "", "db_port": "", "db_password": "",
                   "db_name": "", "db_url": ""}
