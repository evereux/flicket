#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import base64
from datetime import datetime, timedelta
import os
import random
import string

import bcrypt
from flask import url_for
from flask_login import UserMixin

from application import db, app
from application.flicket.models import Base
from application.flicket_api.scripts.paginated_api import PaginatedAPIMixin

user_field_size = {
    'username_min': 4,
    'username_max': 24,
    'name_min': 4,
    'name_max': 60,
    'email_min': 6,
    'email_max': 60,
    'password_min': 6,
    'password_max': 60,
    'group_min': 3,
    'group_max': 64,
    'job_title': 64,
    'avatar': 64
}

flicket_groups = db.Table('flicket_groups',
                          db.Column('user_id', db.Integer, db.ForeignKey('flicket_users.id')),
                          db.Column('group_id', db.Integer, db.ForeignKey('flicket_group.id'))
                          )


class FlicketUser(PaginatedAPIMixin, UserMixin, Base):
    __tablename__ = 'flicket_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(user_field_size['username_max']), index=True, unique=True)
    name = db.Column(db.String(user_field_size['name_max']))
    password = db.Column(db.LargeBinary(user_field_size['password_max']))
    email = db.Column(db.String(user_field_size['email_max']), unique=True)
    date_added = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    job_title = db.Column(db.String(user_field_size['job_title']))
    avatar = db.Column(db.String(user_field_size['avatar']))
    total_posts = db.Column(db.Integer, default=0)
    total_assigned = db.Column(db.Integer, default=0)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    locale = db.Column(db.String(10))
    disabled = db.Column(db.Boolean, default=False)

    def __init__(self, username, name, email, password, date_added, job_title=None, locale='en', disabled=False):
        """
        :param str() username: username, must be unique.
        :param str() name: Full name.
        :param str() email: email address, must be unique.
        :param str() password: password.
        :param str() date_added: date added.
        :param str() job_title: job title / description.
        :param str() locale: locale 'en' = english. See app config for options.
        """
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        self.job_title = job_title
        self.date_added = date_added
        self.locale = locale
        self.disabled = disabled

    @property
    def is_admin(self):
        """

        Returns true if the user is a member of the 'flicket_admin' group.

        :return bool:
        """
        user = FlicketUser.query.filter_by(id=self.id).first()
        for g in user.flicket_groups:
            if g.group_name == app.config['ADMIN_GROUP_NAME']:
                return True
        else:
            return False

    @property
    def is_super_user(self):
        """

        Returns true if the user is a member of the 'super_user' group.

        :return bool:
        """
        user = FlicketUser.query.filter_by(id=self.id).first()
        for g in user.flicket_groups:
            if g.group_name == app.config['SUPER_USER_GROUP_NAME']:
                return True
        else:
            return False

    def check_password(self, password):
        """

        Returns True if password is validated. False if not or is user account is disabled.

        :param password:
        :return bool:
        """
        users = FlicketUser.query.filter_by(username=self.username)
        if users.count() == 0:
            return False
        user = users.first()
        if user.disabled:
            return False
        if bcrypt.hashpw(password.encode('utf-8'), user.password) != user.password:
            return False
        return True

    @staticmethod
    def check_token(token):
        """

        Returns True if token hasn't expired and user account isn't disabled. Otherwise False.

        :param token:
        :return bool:
        """
        user = FlicketUser.query.filter_by(token=token).first()
        if not user.token_expiration:
            return None
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        if user.disabled:
            return None
        return user

    @staticmethod
    def generate_password():
        """
        A pseudo randomly generated password used for registered users wanting to reset their password.

        :return str():
        """

        characters = string.ascii_letters + string.digits
        password = ''.join(random.sample(characters, 12))

        return password

    def get_token(self, expires_in=36000):
        """

        :param expires_in:
        :return str(): self.token
        """
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """
        Method to expire the token. Typically used on logging out.
        :return:
        """
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def to_dict(self):
        """

        Returns a dictionary object about the user.

        :return dict:
        """

        avatar_url = app.config['base_url'] + url_for('flicket_bp.static',
                                                      filename='flicket_avatars/{}'.format("__default_profile.png"))

        if self.avatar:
            avatar_url = app.config['base_url'] + url_for('flicket_bp.static',
                                                          filename='flicket_avatars/{}'.format(self.avatar))

        data = {
            'id': self.id,
            'avatar': avatar_url,
            'email': self.email,
            'job_title': self.job_title if self.job_title else 'unknown',
            'name': self.name,
            'username': self.username,
            'total_posts': self.total_posts,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_user', id=self.id),
                'users': app.config['base_url'] + url_for('bp_api.get_users')
            }
        }

        return data


    def __repr__(self):
        """

        :return: str() with user details.
        """
        return '<User: id={}, username={}, email={}>'.format(self.id, self.username, self.email)


class FlicketGroup(Base):
    """
    Flicket Group model class
    """
    __tablename__ = 'flicket_group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(user_field_size['group_max']))
    users = db.relationship(FlicketUser,
                            secondary=flicket_groups,
                            backref=db.backref('flicket_groups',
                                               lazy='dynamic',
                                               order_by=group_name
                                               )
                            )

    # this is for when a group has many groups
    # ie everyone in group 'flicket_admin' can be a member of group 'all'
    # parents = db.relationship('Group',
    #                           secondary=group_to_group,
    #                           primaryjoin=id==group_to_group.c.parent_id,
    #                           secondaryjoin=id==group_to_group.c.child_id,
    #                           backref="children",
    #                           remote_side=[group_to_group.c.parent_id])

    def __init__(self, group_name):
        """

        :param group_name:
        """
        self.group_name = group_name

    @property
    def __repr__(self):
        """

        :return str():
        """
        return '<Group: id={}. group_name={}>'.format(self.id, self.group_name)
