#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import url_for, g

from application import db
from application.flicket.models import Base
from application.flicket.models.flicket_user import FlicketUser, PaginatedAPIMixin

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


class FlicketStatus(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(field_size['status_max_length']))

    def to_dict(self):
        """
        Returns a dictionary object about the department
        :return:
        """
        data = {
            'id': self.id,
            'status': self.status,
            'links': {
                'self': url_for('bp_api_v2.get_status', id=self.id)
            }
        }

        return data


class FlicketDepartment(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_department'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(field_size['department_max_length']))

    categories = db.relationship('FlicketCategory', back_populates='department')

    # make the default sort order the department name
    __mapper_args__ = {
        "order_by": department.asc()
    }

    def to_dict(self):
        """
        Returns a dictionary object about the department
        :return:
        """
        data = {
            'id': self.id,
            'department': self.department,
            'links': {
                'self': url_for('bp_api_v2.get_department', id=self.id)
            }
        }

        return data


class FlicketCategory(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(field_size['category_max_length']))

    department_id = db.Column(db.Integer, db.ForeignKey(FlicketDepartment.id))
    department = db.relationship(FlicketDepartment, back_populates='categories')

    # make the default sort order the category name
    __mapper_args__ = {
        "order_by": category.asc()
    }

    def to_dict(self):
        """
        Returns a dictionary object about the department
        :return:
        """
        data = {
            'id': self.id,
            'category': self.category,
            'department': self.department.department,
            'links': {
                'self': url_for('bp_api_v2.get_category', id=self.id)
            }
        }

        return data


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
    subscribers = db.relationship('FlicketSubscription', order_by='FlicketSubscription.user_def')

    # finds all the actions associated with the post
    actions = db.relationship('FlicketAction',
                              primaryjoin="and_(FlicketTicket.id == FlicketAction.ticket_id)")

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

    def get_subscriber_emails(self):
        """
        Function to return a list of email addresses of subscribed users.
        :return:
        """
        emails = list()
        for user in self.subscribers:
            emails.append(user.user.email)

        return emails

    @staticmethod
    def query_tickets(form, **kwargs):
        """
        Returns a filtered query and modified form based on form submission
        :param form:
        :param kwargs:
        :return:
        """
        ticket_query = FlicketTicket.query

        for key, value in kwargs.items():

            if key == 'status' and value:
                ticket_query = ticket_query.filter(FlicketTicket.current_status.has(FlicketStatus.status == value))
                form.status.data = FlicketStatus.query.filter_by(status=value).first().id
            if key == 'category' and value:
                ticket_query = ticket_query.filter(FlicketTicket.category.has(FlicketCategory.category == value))
                form.category.data = FlicketCategory.query.filter_by(category=value).first().id
            if key == 'department' and value:
                department_filter = FlicketDepartment.query.filter_by(department=value).first()
                ticket_query = ticket_query.filter(
                    FlicketTicket.category.has(FlicketCategory.department == department_filter))
                form.department.data = department_filter.id
            if key == 'user_id' and value:
                ticket_query = ticket_query.filter_by(assigned_id=int(value))
                user = FlicketUser.query.filter_by(id=value).first()
                form.username.data = user.username
            if key == 'content' and value:
                # search the titles
                form.content.data = key

                f1 = FlicketTicket.title.ilike('%' + value + '%')
                f2 = FlicketTicket.content.ilike('%' + value + '%')
                f3 = FlicketTicket.posts.any(FlicketPost.content.ilike('%' + value + '%'))
                ticket_query = ticket_query.filter(f1 | f2 | f3)

        ticket_query = ticket_query.order_by(FlicketTicket.id.desc())

        return ticket_query, form

    @staticmethod
    def my_tickets(ticket_query):
        """
        Function to return all tickets created by or assigned to user.
        :return:
        """
        ticket_query = ticket_query.filter((FlicketTicket.started_id == g.user.id) | (FlicketTicket.assigned_id == g.user.id)).order_by(FlicketTicket.id.desc())

        return ticket_query

    @staticmethod
    def form_redirect(form, page, url='flicket_bp.tickets'):
        """

        :param form:
        :param page:
        :param url:
        :return:
        """

        department = ''
        category = ''
        status = ''
        user_id = ''

        user = FlicketUser.query.filter_by(username=form.username.data).first()
        if user:
            user_id = user.id

        # convert form inputs to it's table title
        if form.department.data:
            department = FlicketDepartment.query.filter_by(id=form.department.data).first().department
        if form.category.data:
            category = FlicketCategory.query.filter_by(id=form.category.data).first().category
        if form.status.data:
            status = FlicketStatus.query.filter_by(id=form.status.data).first().status

        redirect_url = url_for(url, content=form.content.data,
                               page=page,
                               department=department,
                               category=category,
                               status=status,
                               user_id=user_id)

        return redirect_url


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

    # finds all the actions associated with the post
    actions = db.relationship('FlicketAction',
                              primaryjoin="and_(FlicketPost.id == FlicketAction.post_id)")


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

    user_def = db.deferred(db.select([FlicketUser.name]).where(FlicketUser.id == user_id))

    def __repr__(self):
        return '<Class FlicketSubscription: ticket_id={}, user_id={}>'


class FlicketAction(Base):
    """
    SQL table that stores the action history of a ticket.
    For example, if a user claims a ticket that action is stored here.
    The action is associated with either the ticket_id (if no posts) or post_id (of
    lastest post). The reason for this is displaying within the ticket view.
    """
    __tablename__ = 'flicket_ticket_action'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket)

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost)

    assigned = db.Column(db.Boolean)
    claimed = db.Column(db.Boolean)
    released = db.Column(db.Boolean)
    closed = db.Column(db.Boolean)
    opened = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser, foreign_keys=[user_id])

    recipient_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    recipient = db.relationship(FlicketUser, foreign_keys=[recipient_id])

    date = db.Column(db.DateTime)

    def output_action(self):
        """
        Method used in ticket view to show what action has taken place in ticket.
        :return:
        """

        _date = self.date.strftime('%d-%m-%Y %H:%M')

        if self.assigned:
            return 'Ticket assigned to <a href="mailto:{1}">{0}</a> by <a href="mailto:{3}">{2}</a> | {4}'.format(
                self.recipient.name, self.recipient.email, self.user.name, self.user.email, _date)

        if self.claimed:
            return 'Ticked claimed by <a href="mailto:{}">{}</a>  | {}'.format(self.user.email, self.user.name, _date)

        if self.released:
            return 'Ticket released by <a href="mailto:{}">{}</a> | {}'.format(self.user.email, self.user.name, _date)

        if self.closed:
            return 'Ticked closed by <a href="mailto:{}">{}</a> | {}'.format(self.user.email, self.user.name, _date)

    def __repr__(self):

        return ('<Class FlicketAction: ticket_id={}, post_id={}, assigned={}, unassigned={}, claimed={},'
                'released={}, closed={}, opened={}, user_id={}, recipient_id={}, date={}>').format(self.ticket_id,
                                                                                                   self.post_id,
                                                                                                   self.assigned,
                                                                                                   self.unassigned,
                                                                                                   self.claimed,
                                                                                                   self.released,
                                                                                                   self.closed,
                                                                                                   self.opened,
                                                                                                   self.user_id,
                                                                                                   self.recipient_id,
                                                                                                   self.date)
