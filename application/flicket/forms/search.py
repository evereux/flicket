#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from .flicket_forms import does_user_exist
from application.flicket.models.flicket_models import FlicketDepartment
from application.flicket.models.flicket_models import FlicketCategory
from application.flicket.models.flicket_models import FlicketStatus


class SearchTicketForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        form = super(SearchTicketForm, self).__init__(*args, **kwargs)

        # choices are populated via ajax query on page load. This are simply empty lists so
        # form can be loaded on page view
        self.department.choices = [(d.id, d.department) for d in
                                   FlicketDepartment.query.order_by(FlicketDepartment.department.asc()).all()]
        self.department.choices.insert(0, (0, 'department'))

        self.category.choices = [(c.id, c.category) for c in
                                 FlicketCategory.query.order_by(FlicketCategory.category.asc()).all()]
        self.category.choices.insert(0, (0, 'category'))

        self.status.choices = [(s.id, s.status) for s in FlicketStatus.query.all()]
        self.status.choices.insert(0, (0, 'status'))

    """ Search form. """
    department = SelectField(lazy_gettext('department'), coerce=int, validators=[])
    category = SelectField(lazy_gettext('category'), coerce=int)
    status = SelectField(lazy_gettext('status'), coerce=int)
    username = StringField(lazy_gettext('username'), validators=[does_user_exist])
    content = StringField(lazy_gettext('content'), validators=[])

    def __repr__(self):
        return "<SearchTicketForm>"
