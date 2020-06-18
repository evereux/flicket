#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from sqlalchemy import func, or_
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from application import app
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.hash_password import hash_password
from application.flicket_admin.views.view_admin import create_user
from application.flicket.forms.flicket_forms import form_class_button
from scripts.login_functions import nt_log_on


def login_user_exist(form, field):
    """
    Ensure the username exists.
    :param form:
    :param field:
    :return True False:
    """

    username = form.username.data
    password = form.password.data

    if app.config['use_auth_domain']:
        nt_authenticated = nt_log_on(app.config['auth_domain'], username, password)
    else:
        nt_authenticated = False

    result = FlicketUser.query.filter(
        or_(func.lower(FlicketUser.username) == username.lower(), func.lower(FlicketUser.email) == username.lower()))
    if result.count() == 0:
        # couldn't find username in database so check if the user is authenticated on the domain.
        if nt_authenticated:
            # user might have tried to login with full email?
            username = username.split('@')[0]
            # create the previously unregistered user.
            create_user(username, password, name=username)
        else:
            # user can't be authenticated on the domain or found in the database.
            field.errors.append('Invalid username or email.')
        return False
    result = result.first()
    if bcrypt.hashpw(password.encode('utf-8'), result.password) != result.password:
        if nt_authenticated:
            # update password in database.
            result.password = hash_password(password)
            return True
        field.errors.append('Invalid password. Please contact admin is this problem persists.')
        return False

    return True


def is_disabled(form, field):
    """
    Ensure the username exists.
    :param form:
    :param field:
    :return True False:
    """
    username = form.username.data

    user = FlicketUser.query.filter(
        or_(func.lower(FlicketUser.username) == username.lower(), func.lower(FlicketUser.email) == username.lower()))
    if user.count() == 0:
        return False
    user = user.first()
    if user.disabled:
        field.errors.append('Account has been disabled.')
        return False

    return True


class LogInForm(FlaskForm):
    """ Log in form. """
    username = StringField(lazy_gettext('username'), validators=[DataRequired(), login_user_exist, is_disabled])
    password = PasswordField(lazy_gettext('password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('remember_me'), default=False)


class PasswordResetForm(FlaskForm):
    """ Log in form. """
    email = StringField(lazy_gettext('email'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('reset password'), render_kw=form_class_button)
