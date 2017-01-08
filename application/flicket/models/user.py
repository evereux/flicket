#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime

from application import db, app
from application.home.models import Base

username_maxlength = 24
name_maxlength = 60
email_maxlength = 60

group_maxlength = 64

flicket_groups = db.Table('flicket-groups',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                          db.Column('group_id', db.Integer, db.ForeignKey('flicket-group.id'))
                          )


class User(Base):
    '''
    User model class
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(username_maxlength), index=True, unique=True)
    name = db.Column(db.String(name_maxlength))
    password = db.Column(db.LargeBinary(60))
    email = db.Column(db.String(email_maxlength), unique=True)
    date_added = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __init__(self, username, name, email, password, date_added):
        self.username = username
        self.name = name
        self.password = password
        self.email = email
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
        user = User.query.filter_by(id=self.id).first()
        for g in user.groups:
            if g.group_name == app.config['ADMIN_GROUP_NAME']:
                return True

    def get_id(self):
        return str(self.id)


class FlicketGroup(Base):
    '''
    Flicket Group model class
    '''
    __tablename__ = 'flicket-group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(group_maxlength))
    users = db.relationship(User,
                            secondary=flicket_groups,
                            backref=db.backref('flicket-groups',
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
