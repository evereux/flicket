#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
This rest api is written using flask_rest_jsonapi: http://flask-rest-jsonapi.readthedocs.io/en/latest/
See documentation for usage examples if not explicitly defined below.
"""

from flask import url_for
from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from sqlalchemy.orm.exc import NoResultFound

from application.flicket.models.flicket_user import FlicketUser
from application.flicket.models.flicket_models import FlicketDepartment, FlicketCategory, FlicketStatus
from application import app, db, rest_api


# schemas
class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'user_list'
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    date_added = fields.DateTime()
    date_modified = fields.DateTime()


class DepartmentSchema(Schema):
    class Meta:
        type_ = 'department'
        self_view = 'department_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'department_list'

    id = fields.Str(dump_only=True)
    department = fields.Str(required=True)
    categories = Relationship(
        self_view='department_categories',
        self_view_kwargs={'id': '<id>'},
        related_view='category_list',
        related_view_kwargs={'id': '<id>'},
        many=True,
        schema='CategorySchema',
        type_='category'
    )


class CategorySchema(Schema):
    class Meta:
        type_ = 'category'
        self_view = 'category_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'category_list'

    id = fields.Str(dump_only=True)
    category = fields.Str(required=True)
    department = Relationship(
        attribute='department',
        self_view='category_department',
        self_view_kwargs={'id': '<id>'},
        related_view='department_detail',
        related_view_kwargs={'category_id': '<id>'},
        schema='DepartmentSchema',
        type_='department'
    )


class StatusSchema(Schema):
    class Meta:
        type_ = 'status'
        self_view = 'status_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'status_list'
    id = fields.Str(dump_only=True)
    status = fields.Str(required=True)


# create resource managers
class UserList(ResourceList):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': FlicketUser}


class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': FlicketUser
    }


class DepartmentList(ResourceList):
    schema = DepartmentSchema
    data_layer = {
        'session': db.session,
        'model': FlicketDepartment
    }


class DepartmentDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('category_id') is not None:
            try:
                category = FlicketCategory.query.filter_by(id=view_kwargs['category_id']).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'computer_id'},
                    "Category: {} not found".format(view_kwargs['category_id'])
                )
            else:
                if category.department is not None:
                    view_kwargs['id'] = category.department.id
                else:
                    view_kwargs['id'] = None
    schema = DepartmentSchema
    data_layer = {
        'session': db.session,
        'model': FlicketDepartment,
        'methods': {'before_get_object': before_get_object}
    }


class CategoryList(ResourceList):
    def query(self, view_kwargs):
        query_ = FlicketCategory.query
        if view_kwargs.get('id') is not None:
            try:
                FlicketDepartment.query.filter_by(id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'id'},
                    "Department: {} not found".format(view_kwargs['id'])
                )
            else:
                query_ = query_.join(FlicketDepartment).filter(FlicketDepartment.id == view_kwargs['id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        if view_kwargs.get('id') is not None:
            department = FlicketDepartment.filter_by(id=view_kwargs['id']).one()
            data['department_id'] = department.id

    schema = CategorySchema
    data_layer = {
        'session': db.session,
        'model': FlicketCategory,
        'methods': {'query': query,
                    'before_create_object': before_create_object}
    }


class CategoryDetail(ResourceDetail):
    schema = CategorySchema
    data_layer = {
        'session': db.session,
        'model': FlicketCategory
    }


class StatusList(ResourceList):
    schema = StatusSchema
    data_layer = {
        'session': db.session,
        'model': FlicketStatus
    }


class StatusDetail(ResourceDetail):
    schema = StatusSchema
    data_layer = {
        'session': db.session,
        'model': FlicketStatus
    }


class DepartmentRelationship(ResourceRelationship):
    schema = DepartmentSchema
    data_layer = {
        'session': db.session,
        'model': FlicketDepartment
    }


class CategoryRelationship(ResourceRelationship):
    schema = CategorySchema
    data_layer = {
        'session': db.session,
        'model': FlicketCategory
    }


# User endpoints
rest_api.route(UserList,
               'user_list',
               app.config['FLICKET_REST_API'] + '/users')
rest_api.route(UserDetail,
               'user_detail',
               app.config['FLICKET_REST_API'] + '/user_detail/<int:id>')

# Departments endpoints
rest_api.route(DepartmentList,
               'department_list',
               app.config['FLICKET_REST_API'] + '/departments')
rest_api.route(DepartmentDetail,
               'department_detail',
               app.config['FLICKET_REST_API'] + '/department_detail/<int:id>',
               app.config['FLICKET_REST_API'] + '/categories/<int:category_id>/department')
rest_api.route(DepartmentRelationship,
               'department_categories',
               app.config['FLICKET_REST_API'] + '/departments/<int:id>/relationships/categories')

# Category endpoints
rest_api.route(CategoryList,
               'category_list',
               app.config['FLICKET_REST_API'] + '/categories',
               app.config['FLICKET_REST_API'] + '/departments/<int:id>/categories')
rest_api.route(CategoryDetail,
               'category_detail',
               app.config['FLICKET_REST_API'] + '/category_detail/<int:id>')
rest_api.route(CategoryRelationship,
               'category_department',
               app.config['FLICKET_REST_API'] + '/categories/<int:id>/relationships/department'
)

# Status endpoints
rest_api.route(StatusList,
               'status_list',
               app.config['FLICKET_REST_API'] + '/statuses')
rest_api.route(StatusDetail,
               'status_detail',
               app.config['FLICKET_REST_API'] + '/status_detail/<int:id>')
