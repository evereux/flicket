#! usr/bin/python3
# -*- coding: utf8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    EXPLAIN_TEMPLATE_LOADING = False

    # user login information for database user.
    db_username = 'flicket-db'  # not required for sqlite connection
    db_password = 'cP8OD,PYd5?^gQT0i/ox'  # not required for sqlite connection
    # database connection details
    db_type = 'mysql+pymysql'  # not required for sqlite connection
    db_port = '3306'  # not required for sqlite connection
    db_name = 'flicket-development'

    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@localhost:{}/{}'.format(db_type,
                                                                  db_username,
                                                                  db_password,
                                                                  db_port,
                                                                  db_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    db_field_size = {'ticket': {'title': 50,
                                'description': 5000,
                                'status': 20,
                                'department': 30,
                                'category': 30,
                                'upload_filename': 24,
                                'priority': 12}
                     }

    # default flicket_admin group name
    ADMIN_GROUP_NAME = 'flicket_admin'

    SECRET_KEY = 'lkliaeo239jfj'

    # The base url for your application.
    WEBHOME = '/'
    # The base url for flicket.
    FLICKET = WEBHOME + ''
    FLICKET_API = WEBHOME + 'flicket-api/'
    ADMINHOME = '/flicket_admin/'

    # todo: delete these commented out values if flicket works from db values ok.
    # posts per page
    # posts_per_page = 20

    # ticket system config
    # allowed_extensions = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    #  = 'application/flicket/static/flicket_uploads'
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
