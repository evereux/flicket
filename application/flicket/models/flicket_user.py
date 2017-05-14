#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from application import db, app
from application.flicket.models import Base

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


class FlicketUser(Base):
    """
    User model class
    """
    __tablename__ = 'flicket_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(user_field_size['username_max']), index=True, unique=True)
    name = db.Column(db.String(user_field_size['name_max']))
    password = db.Column(db.LargeBinary(user_field_size['password_max']))
    email = db.Column(db.String(user_field_size['email_max']), unique=True)
    date_added = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    job_title = db.Column(db.String(user_field_size['job_title']))
    avatar = db.Column(db.String(user_field_size['avatar']))

    def __init__(self, username, name, email, password, date_added, job_title=None):
        self.username = username
        self.name = name
        self.password = password
        self.email = email
        self.job_title = job_title
        self.date_added = date_added

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        """ returns true if the user is a member of the 'flicket_admin' group"""
        user = FlicketUser.query.filter_by(id=self.id).first()
        for g in user.flicket_groups:
            if g.group_name == app.config['ADMIN_GROUP_NAME']:
                return True

    def get_id(self):
        return str(self.id)


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
        self.group_name = group_name

    @property
    def __repr__(self):
        return self.group_name
