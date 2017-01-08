#! usr/bin/python3
# -*- coding: utf8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    EXPLAIN_TEMPLATE_LOADING = False

    # user login information for database user.
    username = 'flicket'  # not required for sqlite connection
    password = 'flicket'  # not required for sqlite connection
    # database connection details
    db_type = 'mysql'  # not required for sqlite connection
    db_port = '3306'  # not required for sqlite connection
    db_name = 'flicket-development'

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@localhost:{}/{}'.format(db_type,
                                                                  username,
                                                                  password,
                                                                  db_port,
                                                                  db_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    db_field_size = {'ticket': {'title': 50,
                                'description': 5000,
                                'status': 10,
                                'department': 30,
                                'category': 30,
                                'upload_filename': 24}
                     }

    # default flicket_admin group name
    ADMIN_GROUP_NAME = 'flicket_admin'

    SECRET_KEY = 'lkliaeo239jfj'

    # The base url for your application.
    WEBHOME = '/'
    # The base url for flicket.
    FLICKET = WEBHOME + 'flicket/'
    FLICKET_API = WEBHOME + 'flicket-api/'
    ADMINHOME = '/flicket_admin/'

    # posts per page
    POSTS_PER_PAGE = 20

    # email server
    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # ticket system config
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    TICKET_UPLOAD_FOLDER = 'application/flicket/static/flicket_uploads'
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
