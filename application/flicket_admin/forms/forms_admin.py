#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired
from wtforms.validators import Length

from application import app
from application.flicket.scripts.functions_login import check_email_format
from application.flicket.models.flicket_user import FlicketGroup
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.models.flicket_user import user_field_size


def does_username_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    result = FlicketUser.query.filter_by(username=form.username.data).count()
    if result > 0:
        field.errors.append('The user "{}" is already registered.'.format(form.username.data))
        return False

    return True


def check_username_edit(form, field):
    query = FlicketUser.query.filter_by(id=form.user_id.data).first()

    if form.username.data == query.username:
        return True

    does_username_exist(form, field)


def check_email_edit(form, field):
    query = FlicketUser.query.filter_by(id=form.user_id.data).first()

    if form.email.data == query.email:
        return True

    check_email(form, field)


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
    if not any(s.isupper() for s in field.data) and not any(s.islower() for s in field.data):
        field.errors.append('Password must contain upper and lower characters.')
        ok = False

    return ok


def check_password_edit(form, field):
    """
    If the password has been entered for an edit.
    :param form:
    :param field:
    :return:
    """

    if form.password.data == form.confirm.data == '':
        return True
    check_password_formatting(form, field)


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
        field.errors.append('A user with the email {} is already registered.'.format(form.email.data))
        ok = False

    return ok


class AddUserForm(FlaskForm):
    """ Register user form. """

    def __init__(self, *args, **kwargs):
        form = super(AddUserForm, self).__init__(*args, **kwargs)
        self.locale.choices = [(_id, lang) for _id, lang in app.config['SUPPORTED_LANGUAGES'].items()]

    username = StringField(lazy_gettext('username'),
                           validators=[Length(min=user_field_size['username_min'], max=user_field_size['username_max']),
                                       does_username_exist])
    name = StringField(lazy_gettext('name'),
                       validators=[Length(min=user_field_size['name_min'], max=user_field_size['name_max'])])
    email = StringField(lazy_gettext('email'),
                        validators=[Length(min=user_field_size['email_min'], max=user_field_size['email_max']),
                                    check_email])
    job_title = StringField(lazy_gettext('job_title'), validators=[Length(max=user_field_size['job_title'])])
    password = PasswordField(lazy_gettext('password'), validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        check_password_formatting, Length(min=user_field_size['password_min'], max=user_field_size['password_max'])
    ])
    confirm = PasswordField(lazy_gettext('Repeat Password'))
    locale = SelectField(lazy_gettext('Locale'), validators=[DataRequired()], )
    disabled = BooleanField(lazy_gettext('Disabled'))
    submit = SubmitField(lazy_gettext('add_user'))


class EditUserForm(AddUserForm):
    user_id = HiddenField('user_id')
    username = StringField(lazy_gettext('username'),
                           validators=[Length(min=user_field_size['username_min'], max=user_field_size['username_max']),
                                       check_username_edit])
    email = StringField(lazy_gettext('email'),
                        validators=[Length(min=user_field_size['email_min'], max=user_field_size['email_max']),
                                    check_email_edit])
    job_title = StringField(lazy_gettext('job_title'))
    password = PasswordField(lazy_gettext('password'), validators=[
        EqualTo('confirm', message='Passwords must match'), check_password_edit])
    confirm = PasswordField(lazy_gettext('Repeat Password'))
    groups = SelectMultipleField(lazy_gettext('groups'), coerce=int)
    submit = SubmitField(lazy_gettext('edit_user'))

    def __init__(self, *args, **kwargs):
        form = super(EditUserForm, self).__init__(*args, **kwargs)
        self.groups.choices = [(g.id, g.group_name) for g in FlicketGroup.query.all()]


class AddGroupForm(FlaskForm):
    """ Add group form for flicket_admin section. """
    group_name = StringField(lazy_gettext('group_name'), validators=[
        Length(min=user_field_size['group_min'], max=user_field_size['group_max']),
        DataRequired(),
        group_exists])


class EnterPasswordForm(FlaskForm):
    """
    Form to delete user. User password is required.
    """
    id = HiddenField('id')
    password = PasswordField(lazy_gettext('password'), validators=[DataRequired(), check_password,
                                                                   Length(min=user_field_size['password_min'],
                                                                          max=user_field_size['password_max'])])
