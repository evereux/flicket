#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length

from application.flicket.models.flicket_user import (FlicketGroup,
                                                     FlicketUser,
                                                     username_maxlength,
                                                     name_maxlength,
                                                     email_maxlength,
                                                     group_maxlength)


def group_exists(form, field):
    """ Check whether or not the group still exists.
    :param form:
    :param field:
    :return True / False:
    """
    ok = True
    query = FlicketGroup.query.filter_by(group_name=form.group_name.data).count()
    if query != 0:
        field.errors.append('Group name already exists.')
        ok = False
    return ok


def check_password(form, field):
    """ Is users password correct. """
    ok = True
    result = FlicketUser.query.filter_by(id=form.id.data).first()

    if bcrypt.hashpw(form.password.data.encode('utf-8'), result.password) != result.password:
        field.errors.append('Entered password is incorrect.')
        return False


class EditUserForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        form = super(EditUserForm, self).__init__(*args, **kwargs)
        self.groups.choices = [(g.id, g.group_name) for g in FlicketGroup.query.all()]

    username = StringField('username', validators=[Length(min=4, max=username_maxlength)])
    name = StringField('name', validators=[Length(min=4, max=name_maxlength)])
    email = StringField('email', validators=[Length(min=5, max=email_maxlength)])
    groups = SelectMultipleField('groups', coerce=int)


class AddGroupForm(FlaskForm):
    """ Add group form for flicket_admin section. """
    group_name = StringField('group_name', validators=[
        Length(min=3, max=group_maxlength),
        DataRequired(),
        group_exists])


class EnterPasswordForm(FlaskForm):
    """
    Form to delete user. User password is required.
    """
    id = HiddenField('id')
    password = PasswordField('password', validators=[DataRequired(), check_password])
