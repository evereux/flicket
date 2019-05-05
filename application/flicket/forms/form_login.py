#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired

from application import app
from application.flicket.models.flicket_user import FlicketUser
from application.flicket_admin.views.view_admin import create_user
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

    result = FlicketUser.query.filter_by(username=username)
    if result.count() == 0:
        # couldn't find username in database so check if the user is authenticated on the domain.
        if nt_authenticated:
            # user might have tried to login with full email?
            username = username.split('@')[0]
            # create the previously unregistered user.
            create_user(username, password, name=username)
        else:
            # user can't be authenticated on the domain or found in the database.
            field.errors.append('Invalid username.')
        return False
    result = result.first()
    if bcrypt.hashpw(password.encode('utf-8'), result.password) != result.password:
        if nt_authenticated:
            return True
        field.errors.append('Invalid password. Please contact admin is this problem persists.')
        return False

    return True


class LogInForm(FlaskForm):
    """ Log in form. """
    username = StringField('username', validators=[DataRequired(), login_user_exist])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
