#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from application import db
from application.flicket.models import Base
from application.flicket.models.flicket_user import FlicketUser

# define field sizes. max are used for forms and database. min just for forms.
field_size = {
    'title_min_length': 3,
    'title_max_length': 128,
    'content_min_length': 5,
    'content_max_length': 5000,
    'status_min_length': 3,
    'status_max_length': 20,
    'department_min_length': 3,
    'department_max_length': 30,
    'category_min_length': 3,
    'category_max_length': 30,
    'filename_min_length': 3,
    'filename_max_length': 128,
    'priority_min_length': 3,
    'priority_max_length': 12
}


class FlicketStatus(Base):
    __tablename__ = 'flicket_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(field_size['status_max_length']))


class FlicketDepartment(Base):
    __tablename__ = 'flicket_department'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(field_size['department_max_length']))

    categories = db.relationship('FlicketCategory', back_populates='department')

    # make the default sort order the department name
    __mapper_args__ = {
        "order_by": department.asc()
    }


class FlicketCategory(Base):
    __tablename__ = 'flicket_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(field_size['category_max_length']))

    department_id = db.Column(db.Integer, db.ForeignKey(FlicketDepartment.id))
    department = db.relationship(FlicketDepartment, back_populates='categories')

    # make the default sort order the category name
    __mapper_args__ = {
        "order_by": category.asc()
    }


class FlicketPriority(Base):
    __tablename__ = 'flicket_priorities'

    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(field_size['priority_max_length']))


class FlicketTicket(Base):
    __tablename__ = 'flicket_topic'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(field_size['title_max_length']), index=True)
    content = db.Column(db.String(field_size['content_max_length']))

    started_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser, foreign_keys='FlicketTicket.started_id')

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    modified = db.relationship(FlicketUser, foreign_keys='FlicketTicket.modified_id')

    status_id = db.Column(db.Integer, db.ForeignKey(FlicketStatus.id))
    current_status = db.relationship(FlicketStatus)

    category_id = db.Column(db.Integer, db.ForeignKey(FlicketCategory.id))
    category = db.relationship(FlicketCategory)

    assigned_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    assigned = db.relationship(FlicketUser, foreign_keys='FlicketTicket.assigned_id')

    ticket_priority_id = db.Column(db.Integer, db.ForeignKey(FlicketPriority.id))
    ticket_priority = db.relationship(FlicketPriority)

    posts = db.relationship("FlicketPost", back_populates="ticket")

    # find all the images associated with the topic
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketTicket.id == FlicketUploads.topic_id)")

    # finds all the users who are subscribed to the ticket.
    subscribers = db.relationship('FlicketSubscription')

    @property
    def num_replies(self):
        n_replies = FlicketPost.query.filter_by(ticket_id=self.id).count()
        return n_replies

    @property
    def id_zfill(self):
        return str(self.id).zfill(5)

    def is_subscribed(self, user):
        for s in self.subscribers:
            if s.user == user:
                return True
        return False



class FlicketPost(Base):
    __tablename__ = 'flicket_post'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket, back_populates='posts')

    content = db.Column(db.String(field_size['content_max_length']))

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser, foreign_keys='FlicketPost.user_id')

    date_added = db.Column(db.DateTime())
    date_modified = db.Column(db.DateTime())

    modified_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    modified = db.relationship(FlicketUser, foreign_keys='FlicketPost.modified_id')

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

    filename = db.Column(db.String(field_size['filename_max_length']))
    original_filename = db.Column(db.String(field_size['filename_max_length']))


class FlicketHistory(Base):
    __tablename__ = 'flicket_history'

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket)

    date_modified = db.Column(db.DateTime())

    original_content = db.Column(db.String(field_size['content_max_length']))

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser)


class FlicketSubscription(Base):
    __tablename__ = 'flicket_ticket_subscription'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket)

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser)