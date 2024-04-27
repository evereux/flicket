#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import url_for, g
from sqlalchemy import select, join, func

from application import app, db
from application.flicket.models import Base
from application.flicket.models.flicket_user import FlicketUser
from application.flicket_api.scripts.paginated_api import PaginatedAPIMixin

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
    'priority_max_length': 12,
    'action_max_length': 30,
}


class FlicketStatus(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(field_size['status_max_length']))

    def to_dict(self):
        """
        Returns a dictionary object about the status
        :return:
        """
        data = {
            'id': self.id,
            'status': self.status,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_status', id=self.id),
                'statuses': app.config['base_url'] + url_for('bp_api.get_statuses'),
            }
        }

        return data

    def __repr__(self):
        return "<FlicketStatus: id={}, status={}>".format(self.id, self.status)


class FlicketDepartment(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_department'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(field_size['department_max_length']))
    categories = db.relationship('FlicketCategory', back_populates='department')

    def __init__(self, department):
        """

        :param department:
        """
        self.department = department

    def to_dict(self):
        """
        Returns a dictionary object about the department
        :return:
        """
        data = {
            'id': self.id,
            'department': self.department,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_department', id=self.id),
                'departments': app.config['base_url'] + url_for('bp_api.get_departments'),
            }
        }

        return data

    def __repr__(self):
        return "<FlicketDepartment: id={}, department={}>".format(self.id, self.department)


class FlicketCategory(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(field_size['category_max_length']))

    department_id = db.Column(db.Integer, db.ForeignKey(FlicketDepartment.id))
    department = db.relationship(FlicketDepartment, back_populates='categories')

    def __init__(self, category, department):
        """

        :param category:
        """
        self.category = category
        self.department = department

    def to_dict(self):
        """
        Returns a dictionary object about the category and its department
        :return:
        """
        data = {
            'id': self.id,
            'category': self.category,
            'department': self.department.department,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_category', id=self.id),
                'categories': app.config['base_url'] + url_for('bp_api.get_categories'),
                'department': app.config['base_url'] + url_for('bp_api.get_department', id=self.department_id),
            }
        }

        return data

    def __repr__(self):
        return "<FlicketCategory: id={}, category={}>".format(self.id, self.category)


class FlicketPriority(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_priorities'

    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(field_size['priority_max_length']))

    def to_dict(self):
        """
        Returns a dictionary object about the category and its department
        :return:
        """
        data = {
            'id': self.id,
            'priority': self.priority,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_priority', id=self.id),
                'priorities': app.config['base_url'] + url_for('bp_api.get_priorities')
            }
        }

        return data

    def __repr__(self):
        return "<FlicketPriority: id={}, priority={}>".format(self.id, self.priority)


class FlicketTicket(PaginatedAPIMixin, Base):
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

    hours = db.Column(db.Numeric(10, 2), server_default='0')

    last_updated = db.Column(db.DateTime(), server_default=datetime.datetime.now().strftime('%Y-%m-%d'))

    # find all the images associated with the topic
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketTicket.id == FlicketUploads.topic_id)")

    # finds all the users who are subscribed to the ticket.
    subscribers = db.relationship('FlicketSubscription', order_by='FlicketSubscription.user_def')

    # finds all the actions associated with the ticket
    actions = db.relationship('FlicketAction',
                              primaryjoin="FlicketTicket.id == FlicketAction.ticket_id")

    # finds all the actions associated with the ticket and not associated with any post
    actions_nonepost = db.relationship('FlicketAction',
                                       primaryjoin="and_(FlicketTicket.id == FlicketAction.ticket_id, "
                                                   "FlicketAction.post_id == None)",
                                       overlaps="actions")

    @property
    def num_replies(self):
        n_replies = FlicketPost.query.filter_by(ticket_id=self.id).count()
        return n_replies

    @property
    def id_zfill(self):
        return str(self.id).zfill(5)

    @property
    def department_category(self):
        return f'{self.category.department.department} / {self.category.category}'

    def is_subscribed(self, user):
        for s in self.subscribers:
            if s.user == user:
                return True
        return False

    def can_unsubscribe(self, user):
        """

        Return true if user is admin, super_user or is trying to unsubscribe them self.

        :param user:
        :return:
        """
        if any([g.user.is_admin, g.user.is_super_user]) and self.is_subscribed(user):
            return True

        if self.is_subscribed(user) and user.id == g.user.id:
            return True

        return False

    @staticmethod
    def carousel_query():
        """
        Return all 'open' 'high priority' tickets for carousel.
        :return:
        """

        tickets = FlicketTicket.query.filter(FlicketTicket.ticket_priority_id == 3). \
            filter(FlicketTicket.status_id == 1).limit(100)

        return tickets

    @staticmethod
    def form_redirect(form, url='flicket_bp.tickets'):
        """

        :param form:
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
                               department=department,
                               category=category,
                               status=status,
                               user_id=user_id)

        return redirect_url

    @property
    def total_hours(self):
        """
        Sums all hours related to ticket (posts + ticket itself).
        :return:
        """

        hours = db.session.query(func.sum(FlicketPost.hours)).filter_by(ticket_id=self.id).scalar() or 0

        return hours + self.hours

    def get_subscriber_emails(self):
        """
        Function to return a list of email addresses of subscribed users.
        :return:
        """
        emails = list()
        for subscriber in self.subscribers:
            if not subscriber.user.disabled:
                emails.append(subscriber.user.email)

        return emails

    @staticmethod
    def my_tickets(ticket_query):
        """
        Function to return all tickets created by or assigned to user.
        :return:
        """
        ticket_query = ticket_query.filter(
            (FlicketTicket.started_id == g.user.id) | (FlicketTicket.assigned_id == g.user.id))

        return ticket_query

    @staticmethod
    def my_subscribed_tickets(ticket_query):
        """
        Function to return all tickets subscribed to by user.
        :return: query
        """

        return ticket_query.filter(FlicketTicket.subscribers.any(FlicketSubscription.user_id == g.user.id))

    @staticmethod
    def query_tickets(form=None, **kwargs):
        """
        Returns a filtered query and modified form based on form submission
        :param form:
        :param kwargs:
        :return:
        """

        ticket_query = FlicketTicket.query

        if kwargs['status']:
            ticket_query = ticket_query.filter(FlicketTicket.current_status.has(FlicketStatus.status != 'Closed'))

        if 'assigned_id' in kwargs:
            if kwargs['assigned_id']:
                ticket_query = ticket_query.filter_by(assigned_id=kwargs['assigned_id'])

        if 'created_id' in kwargs:
            if kwargs['created_id']:
                ticket_query = ticket_query.filter_by(started_id=kwargs['created_id'])

        for key, value in kwargs.items():

            if key == 'status' and value:
                ticket_query = ticket_query.filter(FlicketTicket.current_status.has(FlicketStatus.status == value))
                if form:
                    form.status.data = FlicketStatus.query.filter_by(status=value).first().id

            if key == 'category' and value:
                ticket_query = ticket_query.filter(FlicketTicket.category.has(FlicketCategory.category == value))
                if form:
                    form.category.data = FlicketCategory.query.filter_by(category=value).first().id

            if key == 'department' and value:
                department_filter = FlicketDepartment.query.filter_by(department=value).first()
                ticket_query = ticket_query.filter(
                    FlicketTicket.category.has(FlicketCategory.department == department_filter))
                if form:
                    form.department.data = department_filter.id

            if key == 'user_id' and value:
                # ticket_query = ticket_query.filter_by(assigned_id=int(value))
                ticket_query = ticket_query.filter(
                    (FlicketTicket.assigned_id == int(value)) | (FlicketTicket.started_id == int(value)))
                user = FlicketUser.query.filter_by(id=value).first()
                if form:
                    form.username.data = user.username

            if key == 'content' and value:
                # search the titles
                if form:
                    form.content.data = key

                f1 = FlicketTicket.title.ilike('%' + value + '%')
                f2 = FlicketTicket.content.ilike('%' + value + '%')
                f3 = FlicketTicket.posts.any(FlicketPost.content.ilike('%' + value + '%'))
                ticket_query = ticket_query.filter(f1 | f2 | f3)

        return ticket_query, form

    @staticmethod
    def sorted_tickets(ticket_query, sort):
        """
        Function to return sorted tickets.
        :param ticket_query:
        :param sort:
        :return:
        """
        if sort == 'priority':
            ticket_query = ticket_query.order_by(FlicketTicket.ticket_priority_id, FlicketTicket.id)
        elif sort == 'priority_desc':
            ticket_query = ticket_query.order_by(FlicketTicket.ticket_priority_id.desc(), FlicketTicket.id)

        elif sort == 'title':
            ticket_query = ticket_query.order_by(FlicketTicket.title, FlicketTicket.id)
        elif sort == 'title_desc':
            ticket_query = ticket_query.order_by(FlicketTicket.title.desc(), FlicketTicket.id)

        elif sort == 'ticketid':
            ticket_query = ticket_query.order_by(FlicketTicket.id)
        elif sort == 'ticketid_desc':
            ticket_query = ticket_query.order_by(FlicketTicket.id.desc())

        elif sort == 'addedby':
            ticket_query = ticket_query.join(FlicketUser, FlicketTicket.user) \
                .order_by(FlicketUser.name, FlicketTicket.id)
        elif sort == 'addedby_desc':
            ticket_query = ticket_query.join(FlicketUser, FlicketTicket.user) \
                .order_by(FlicketUser.name.desc(), FlicketTicket.id)

        elif sort == 'addedon':
            ticket_query = ticket_query.order_by(FlicketTicket.date_added, FlicketTicket.id)
        elif sort == 'addedon_desc':
            ticket_query = ticket_query.order_by(FlicketTicket.date_added.desc(), FlicketTicket.id)

        elif sort == 'last_updated':
            ticket_query = ticket_query.order_by(FlicketTicket.last_updated, FlicketTicket.id)
        elif sort == 'last_updated_desc':
            ticket_query = ticket_query.order_by(FlicketTicket.last_updated.desc(), FlicketTicket.id)

        elif sort == 'replies':
            replies_count = func.count(FlicketPost.id).label('replies_count')
            ticket_query = ticket_query.outerjoin(FlicketTicket.posts).group_by(FlicketTicket.id) \
                .order_by(replies_count, FlicketTicket.id)
        elif sort == 'replies_desc':
            replies_count = func.count(FlicketPost.id).label('replies_count')
            ticket_query = ticket_query.outerjoin(FlicketTicket.posts).group_by(FlicketTicket.id) \
                .order_by(replies_count.desc(), FlicketTicket.id)

        elif sort == 'department_category':
            ticket_query = ticket_query.join(FlicketCategory, FlicketTicket.category) \
                .join(FlicketDepartment, FlicketCategory.department) \
                .order_by(FlicketDepartment.department, FlicketCategory.category, FlicketTicket.id)
        elif sort == 'department_category_desc':
            ticket_query = ticket_query.join(FlicketCategory, FlicketTicket.category) \
                .join(FlicketDepartment, FlicketCategory.department) \
                .order_by(FlicketDepartment.department.desc(), FlicketCategory.category.desc(), FlicketTicket.id)

        elif sort == 'status':
            ticket_query = ticket_query.order_by(FlicketTicket.status_id, FlicketTicket.id)
        elif sort == 'status_desc':
            ticket_query = ticket_query.order_by(FlicketTicket.status_id.desc(), FlicketTicket.id)

        elif sort == 'assigned':
            ticket_query = ticket_query.outerjoin(FlicketUser, FlicketTicket.assigned) \
                .order_by(FlicketUser.name, FlicketTicket.id)
        elif sort == 'assigned_desc':
            ticket_query = ticket_query.outerjoin(FlicketUser, FlicketTicket.assigned) \
                .order_by(FlicketUser.name.desc(), FlicketTicket.id)

        elif sort == 'time':
            total_hours = (FlicketTicket.hours + func.sum(FlicketPost.hours)).label('total_hours')
            ticket_query = ticket_query.outerjoin(FlicketTicket.posts).group_by(FlicketTicket.id) \
                .order_by(total_hours, FlicketTicket.id)
        elif sort == 'time_desc':
            total_hours = (FlicketTicket.hours + func.sum(FlicketPost.hours)).label('total_hours')
            ticket_query = ticket_query.outerjoin(FlicketTicket.posts).group_by(FlicketTicket.id) \
                .order_by(total_hours.desc(), FlicketTicket.id)

        return ticket_query

    def from_dict(self, data):
        """

        :param data:
        :return:
        """
        for field in ['title', 'content', 'category_id', 'ticket_priority_id']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        """

        :return: dict()
        """

        modified_by = None
        assigned = None

        if self.modified_id:
            modified_by = app.config['base_url'] + url_for('bp_api.get_user', id=self.modified_id)

        if self.assigned_id:
            assigned = app.config['base_url'] + url_for('bp_api.get_user', id=self.assigned_id)

        data = {
            'id': self.id,
            'assigned_id': self.assigned_id,
            'category_id': self.category_id,
            'content': self.content,
            'date_added': self.date_added,
            'date_modified': self.date_modified,
            'modified_id': self.modified_id,
            'started_id': self.started_id,
            'status_id': self.status_id,
            'title': self.title,
            'ticket_priority_id': self.ticket_priority_id,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_ticket', id=self.id),
                'assigned': assigned,
                'priority': app.config['base_url'] + url_for('bp_api.get_priority', id=self.ticket_priority_id),
                'started_ny': app.config['base_url'] + url_for('bp_api.get_user', id=self.started_id),
                'modified_by': modified_by,
                'category': app.config['base_url'] + url_for('bp_api.get_category', id=self.category_id),
                'status': app.config['base_url'] + url_for('bp_api.get_status', id=self.status_id),
                'subscribers': app.config['base_url'] + url_for('bp_api.get_subscriptions', ticket_id=self.id),
                'tickets': app.config['base_url'] + url_for('bp_api.get_tickets'),
                'histories': app.config['base_url'] + url_for('bp_api.get_histories', topic_id=self.id),
            }

        }

        return data

    def __repr__(self):
        return (f'<FlicketTicket: '
                f'id={self.id}, '
                f'title="{self.title}", '
                f'created_by={self.user}, '
                f'category={self.category}'
                f'status={self.current_status}'
                f'assigned={self.assigned}>')


class FlicketPost(PaginatedAPIMixin, Base):
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

    hours = db.Column(db.Numeric(10, 2), server_default='0')

    # finds all the images associated with the post
    uploads = db.relationship('FlicketUploads',
                              primaryjoin="and_(FlicketPost.id == FlicketUploads.posts_id)")

    # finds all the actions associated with the post
    actions = db.relationship('FlicketAction',
                              primaryjoin="FlicketPost.id == FlicketAction.post_id")

    def to_dict(self):
        """

        :return: dict()
        """

        data = {
            'id': self.id,
            'content': self.content,
            'data_added': self.date_added,
            'date_modified': self.date_modified,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_post', id=self.id),
                'created_by': app.config['base_url'] + url_for('bp_api.get_user', id=self.user_id),
                'posts': app.config['base_url'] + url_for('bp_api.get_posts', ticket_id=self.ticket_id),
            }

        }

        return data

    def __repr__(self):
        return "<FlicketPost: id={}, ticket_id={}, content={}>".format(self.id, self.ticket_id, self.content)


class FlicketUploads(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_uploads'

    id = db.Column(db.Integer, primary_key=True)

    posts_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost, overlaps="uploads")

    topic_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    topic = db.relationship(FlicketTicket, overlaps="uploads")

    filename = db.Column(db.String(field_size['filename_max_length']))
    original_filename = db.Column(db.String(field_size['filename_max_length']))

    def to_dict(self):
        """

        :return: dict()
        """

        ticket_url, post_url = None, None

        if self.topic_id:
            ticket_url = app.config['base_url'] + url_for('bp_api.get_ticket', id=self.topic_id)

        if self.posts_id:
            post_url = app.config['base_url'] + url_for('bp_api.get_post', id=self.posts_id)

        data = {
            'id': self.id,
            'filename': self.filename,
            'image': app.config['base_url'] + '/flicket_uploads/' + self.filename,
            'original_filename': self.original_filename,
            'post_id': self.posts_id,
            'topic_id': self.topic_id,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_upload', id=self.id),
                'post': post_url,
                'ticket': ticket_url,
                'uploads': app.config['base_url'] + url_for('bp_api.get_uploads'),
            }

        }

        return data

    def __repr__(self):
        return ("<FlicketUploads: id={}, "
                "post_id={}, topic_id={}, filename={}, original_filename={}>").format(self.id,
                                                                                      self.posts_id,
                                                                                      self.topic_id,
                                                                                      self.filename,
                                                                                      self.original_filename)


class FlicketHistory(PaginatedAPIMixin, Base):
    """
        A database to track the editing of tickets and posts.
    """
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

    def to_dict(self):
        """

        :return: dict()
        """

        ticket_url, post_url = None, None

        if self.topic_id:
            ticket_url = app.config['base_url'] + url_for('bp_api.get_ticket', id=self.topic_id)

        if self.post_id:
            post_url = app.config['base_url'] + url_for('bp_api.get_post', id=self.post_id)

        data = {
            'id': self.id,
            'date_modified': self.date_modified,
            'original_content': self.original_content,
            'post_id': self.post_id,
            'topic_id': self.topic_id,
            'user_id': self.user_id,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_history', id=self.id),
                'histories': app.config['base_url'] + url_for('bp_api.get_histories'),
                'post': post_url,
                'ticket': ticket_url,
                'user': app.config['base_url'] + url_for('bp_api.get_user', id=self.user_id),
            }

        }

        return data

    def __repr__(self):
        return "<FlicketHistory: id={}, post_id={}, topic_id={}>".format(self.id, self.posts_id, self.topic_id)


class FlicketSubscription(PaginatedAPIMixin, Base):
    __tablename__ = 'flicket_ticket_subscription'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket, overlaps="subscribers")

    user_id = db.Column(db.Integer, db.ForeignKey(FlicketUser.id))
    user = db.relationship(FlicketUser)

    user_def = db.deferred(db.select(FlicketUser.name).where(FlicketUser.id == user_id).scalar_subquery())

    def to_dict(self):
        """

        :return: dict()
        """

        data = {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'user_def': self.user_def,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_subscription', id=self.id),
                'subscriptions': app.config['base_url'] + url_for('bp_api.get_subscriptions'),
                'ticket': app.config['base_url'] + url_for('bp_api.get_ticket', id=self.ticket_id),
                'user': app.config['base_url'] + url_for('bp_api.get_user', id=self.user_id),
            }

        }

        return data

    def __repr__(self):
        return '<Class FlicketSubscription: ticket_id={}, user_id={}>'.format(self.ticket_id, self.user_id)


class FlicketAction(PaginatedAPIMixin, Base):
    """
    SQL table that stores the action history of a ticket.
    For example, if a user claims a ticket that action is stored here.
    The action is associated with ticket_id and latest post_id (if exists).
    """
    __tablename__ = 'flicket_ticket_action'

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.Integer, db.ForeignKey(FlicketTicket.id))
    ticket = db.relationship(FlicketTicket, overlaps="actions, actions_nonepost")

    post_id = db.Column(db.Integer, db.ForeignKey(FlicketPost.id))
    post = db.relationship(FlicketPost, overlaps="actions")

    action = db.Column(db.String(field_size['action_max_length']))
    data = db.Column(db.JSON(none_as_null=True))

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

        if self.action == 'open':
            return (f'Ticket opened'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'assign':
            return (f'Ticket assigned to <a href="mailto:{self.recipient.email}">{self.recipient.name}</a>'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'claim':
            return (f'Ticked claimed'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'status':
            return (f'Ticket status has been changed to "{self.data["status"]}"'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'priority':
            return (f'Ticket priority has been changed to "{self.data["priority"]}"'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'release':
            return (f'Ticket released'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'close':
            return (f'Ticked closed'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'department_category':
            return (f'Ticket category has been changed to "{self.data["department_category"]}"'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a> | {_date}')

        if self.action == 'subscribe':
            return (f'<a href="mailto:{self.recipient.email}">{self.recipient.name}</a> has been subscribed to ticket'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a>. | {_date}')

        if self.action == 'unsubscribe':
            return (f'<a href="mailto:{self.recipient.email}">{self.recipient.name}</a> '
                    f'has been un-subscribed from ticket'
                    f' by <a href="mailto:{self.user.email}">{self.user.name}</a>. | {_date}')

    def to_dict(self):
        """

        :return: dict()
        """

        data = {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'post_id': self.post_id,
            'action': self.action,
            'data': self.data,
            'user_id': self.user_id,
            'recipient_id': self.recipient_id,
            'date': self.date,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_action', id=self.id),
                'actions': app.config['base_url'] + url_for('bp_api.get_actions', ticket_id=self.ticket_id),
            }
        }

        return data

    def __repr__(self):
        return (f'<Class FlicketAction: ticket_id={self.ticket_id}, post_id={self.ticket_id}, action={self.action!r}, '
                f'data={self.data}, user_id={self.user_id}, recipient_id={self.recipient_id}, date={self.date}>')


# Virtual Model Flicket DepartmentCategory
# xdml: as not sure how to best implement it, I created "Virtual Model" or how to call it
# that is similar to SQL VIEW, it is simple SELECT FROM flicket_category JOIN flicket_department
# query, setting primary_key, so Flask SqlAlchemy ORM can be used as on regular SQL table
class FlicketDepartmentCategory(PaginatedAPIMixin, Base):
    __table__ = select(
        func.concat(FlicketDepartment.department, ' / ', FlicketCategory.category).label('department_category'),
        FlicketCategory.id.label('category_id'),
        FlicketCategory.category.label('category'),
        FlicketDepartment.id.label('department_id'),
        FlicketDepartment.department.label('department')
    ).select_from(join(
        FlicketCategory,
        FlicketDepartment,
        FlicketCategory.department_id == FlicketDepartment.id)
    ).alias()
    __mapper_args__ = {
        'primary_key': FlicketCategory.id
    }

    def to_dict(self):
        data = {
            'department_category': self.department_category,
            'category_id': self.category_id,
            'category': self.category,
            'department_id': self.department_id,
            'department': self.department,
            'links': {
                'self': app.config['base_url'] + url_for('bp_api.get_department_category', id=self.category_id),
                'department_categories': app.config['base_url'] + url_for('bp_api.get_department_categories'),
                'department': app.config['base_url'] + url_for('bp_api.get_department', id=self.department_id),
                'category': app.config['base_url'] + url_for('bp_api.get_category', id=self.category_id),
            },
        }

        return data

    def __repr__(self):
        return (f"<FlicketDepartmentCategory: department_category='{self.department_category}',"
                f" category_id={self.category_id}>")
