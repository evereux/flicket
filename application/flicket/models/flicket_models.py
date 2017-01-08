#! usr/bin/python3
# -*- coding: utf8 -*-

from application import db
from application.flicket.models.user import User
from config import BaseConfiguration

Base = db.Model


class FlicketStatus(Base):
    __tablename__ = 'flicket_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['status']))


class FlicketDepartment(Base):
    __tablename__ = 'flicket_department'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['department']))

    categories = db.relationship('FlicketCategory', back_populates='department')


class FlicketCategory(Base):
    __tablename__ = 'flicket_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['category']))

    department_id = db.Column(db.Integer, db.ForeignKey(FlicketDepartment.id))
    department = db.relationship(FlicketDepartment, back_populates='categories')


class FlicketPriority(Base):
    __tablename__ = 'flicket_priorities'

    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(12))


class FlicketTicket(Base):
    __tablename__ = 'flicket_topic'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['title']), index=True)
    content = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['description']))

    started_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys='FlicketTicket.started_id')

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_id = db.Column(db.Integer, db.ForeignKey(User.id))
    modified = db.relationship(User, foreign_keys='FlicketTicket.modified_id')

    status_id = db.Column(db.Integer, db.ForeignKey(FlicketStatus.id))
    current_status = db.relationship(FlicketStatus)

    category_id = db.Column(db.Integer, db.ForeignKey(FlicketCategory.id))
    category = db.relationship(FlicketCategory)

    assigned_id = db.Column(db.Integer, db.ForeignKey(User.id))
    assigned = db.relationship(User, foreign_keys='FlicketTicket.assigned_id')

    ticket_priority_id = db.Column(db.Integer, db.ForeignKey(FlicketPriority.id))
    ticket_priority = db.relationship(FlicketPriority)

    posts = db.relationship("FlicketPost", back_populates="ticket")

    # find all the images associated with the topic
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketTicket.id == FlicketUploads.topic_id)")

    @property
    def replies(self):
        num_replies = FlicketPost.query.filter_by(ticket_id=self.id).count()
        return num_replies

    @property
    def id_zfill(self):
        return str(self.id).zfill(5)


class FlicketPost(Base):
    __tablename__ = 'flicket_post'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket, back_populates='posts')

    content = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['description']))

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys='FlicketPost.user_id')

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_by = db.Column(db.Integer, db.ForeignKey(User.id))
    modified = db.relationship(User, foreign_keys='FlicketPost.modified_by')

    # finds all the images associated with the post
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketPost.id == FlicketUploads.posts_id)")


class FlicketUploads(Base):
    __tablename__ = 'flicket_uploads'

    id = db.Column(db.Integer, primary_key=True)

    posts_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket)

    filename = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['upload_filename']))
    original_filename = db.Column(db.String(BaseConfiguration.db_field_size['ticket']['upload_filename']))
