#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from .flicket_forms import does_user_exist
from application.flicket.models.flicket_models import FlicketDepartment, FlicketCategory, FlicketStatus


class SearchTicketForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        form = super(SearchTicketForm, self).__init__(*args, **kwargs)

        # choices are populated via ajax query on page load. This are simply empty lists so
        # form can be loaded on page view
        self.department.choices = [(d.id, d.department) for d in FlicketDepartment.query.all()]
        self.department.choices.insert(0, (0, 'department'))

        self.category.choices = [(c.id, c.category) for c in FlicketCategory.query.all()]
        self.category.choices.insert(0, (0, 'category'))

        self.status.choices = [(s.id, s.status) for s in FlicketStatus.query.all()]
        self.status.choices.insert(0, (0, 'status'))

    """ Search form. """
    department = SelectField('department', coerce=int, validators=[])
    category = SelectField('category', coerce=int)
    status = SelectField('status', coerce=int)
    username = StringField('username', validators=[does_user_exist])
    content = StringField('content', validators=[])