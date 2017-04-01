#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from .flicket_forms import does_email_exist
from application.flicket_api.scripts.api_class import FlicketApi


class SearchTicketForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        form = super(SearchTicketForm, self).__init__(*args, **kwargs)

        # choices are populated via ajax query on page load. This are simply empty lists so
        # form can be loaded on page view
        self.department.choices = []
        self.department.choices.insert(0, (0, 'department'))

        self.category.choices = []
        self.category.choices.insert(0, (0, 'category'))

        self.status.choices = []
        self.status.choices.insert(0, (0, 'status'))

    """ Search form. """
    department = SelectField('department', coerce=int)
    category = SelectField('category', coerce=int)
    status = SelectField('status', coerce=int)
    email = StringField('email', validators=[does_email_exist])
    content = StringField('content', validators=[])