#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo

from application.flicket.scripts.functions_login import check_email_format
from application.flicket.models.flicket_user import (FlicketGroup,
                                                     FlicketUser,
                                                     username_maxlength,
                                                     name_maxlength,
                                                     email_maxlength,
                                                     group_maxlength)


def does_username_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    result = FlicketUser.query.filter_by(username=form.username.data).count()
    if result > 0:
        field.errors.append('A user with this username has already registered.')
        return False

    return True


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
    """
    Check formatting of password.
    :param form:
    :param field:
    :return True / False:
    """
    result = FlicketUser.query.filter_by(id=form.id.data).first()
    if bcrypt.hashpw(form.password.data.encode('utf-8'), result.password) != result.password:
        field.errors.append('Entered password is incorrect.')
        return False
    return True


def check_password_formatting(form, field):
    """
    Check formatting of password.
    :param form:
    :param field:
    :return True / False:
    """
    ok = True
    _min = 6
    if len(field.data) < _min:
        field.errors.append('Password must be more than {} characters.'.format(min))
        ok = False
    if not any(s.isupper() for s in field.data) and not any(s.islower() for s in field.data):
        field.errors.append('Password must contain upper and lower characters.')
        ok = False

    return ok


def check_email(form, field):
    """
    Checks formatting of email and also checks that a user is not already registered with the same email address
    :param form:
    :param field:
    :return:
    """
    ok = True
    if not check_email_format(field.data):
        field.errors.append('Please enter a correctly formatted email address.')
        ok = False
    result = FlicketUser.query.filter_by(email=form.email.data).count()
    if result > 0:
        field.errors.append('A user with this email address is already registered.')
        ok = False

    return ok


class RegisterForm(FlaskForm):
    """ Register user form. """
    username = StringField('username', validators=[Length(min=4, max=username_maxlength), does_username_exist])
    name = StringField('name', validators=[Length(min=4, max=name_maxlength)])
    email = StringField('email', validators=[Length(min=5, max=email_maxlength), check_email])
    password = PasswordField('password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        check_password_formatting
    ])
    confirm = PasswordField('Repeat Password')


class EditUserForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        form = super(EditUserForm, self).__init__(*args, **kwargs)
        self.groups.choices = [(g.id, g.group_name) for g in FlicketGroup.query.all()]

    username = StringField('username', validators=[Length(min=4, max=username_maxlength)])
    name = StringField('name', validators=[Length(min=4, max=name_maxlength)])
    email = StringField('email', validators=[Length(min=5, max=email_maxlength), check_email])
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
