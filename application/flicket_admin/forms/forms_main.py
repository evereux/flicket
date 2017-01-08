#! usr/bin/python3
# -*- coding: utf8 -*-

import bcrypt
from flask import g
from flask_wtf import FlaskForm
from wtforms import (PasswordField,
                     StringField, )
from wtforms.validators import (DataRequired,
                                Length,
                                EqualTo)

from application.flicket.models.user import (User,
                                             username_maxlength,
                                             name_maxlength,
                                             email_maxlength)
from application.flicket.scripts.functions_login import check_email_format


def does_username_exist(form, field):
    """
    Username must be unique so we check against the database to ensure it doesn't
    :param form:
    :param field:
    :return True / False:
    """
    result = User.query.filter_by(username=form.username.data).count()
    if result > 0:
        field.errors.append('A user with this username has already registered.')
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
    min = 6
    if (len(field.data) < min):
        field.errors.append('Password must be more than {} characters.'.format(min))
        ok = False
    if not any(s.isupper() for s in field.data) and not any(s.islower() for s in field.data):
        field.errors.append('Password must contain upper and lower characters.')
        ok = False

    return ok


def check_password(form, field):
    """
    Check formatting of password.
    :param form:
    :param field:
    :return True / False:
    """
    ok = True
    result = User.query.filter_by(username=g.user.username).first()
    if bcrypt.hashpw(form.password.data.encode('utf-8'), result.password) != result.password:
        field.errors.append('Entered password is incorrect.')
        return False
    return ok


def check_email(form, field):
    ok = True
    if not check_email_format(field.data):
        field.errors.append('Please enter a valid email address.')
        ok = False
    result = User.query.filter_by(email=form.email.data).count()
    if result > 0:
        field.errors.append('A user with this email address has already registered.')
        ok = False

    return ok


def change_email(form, field):
    ok = True

    if form.email.data == g.user.email:
        return True

    check_email(form, field)


class CheckPasswordCorrect(object):
    # check if password exists
    def __call__(self, form, field):
        self.username = form.username.data
        self.password = form.password.data
        self.password = self.password.encode('utf-8')
        ok = True
        user = User.query.filter_by(username=form.username.data).first()
        # hashed = user.password
        if user and not bcrypt.hashpw(self.password, user.password) == user.password:
            field.errors.append('Your username and password do not match those in the database.')
            ok = False

        return ok


class RegisterForm(FlaskForm):
    """ Register user form. """
    username = StringField('username', validators=[Length(min=4, max=username_maxlength), does_username_exist])
    name = StringField('name', validators=[Length(min=4, max=name_maxlength)])
    email = StringField('email', validators=[Length(min=5, max=email_maxlength)])
    password = PasswordField('password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        check_password_formatting
    ])
    confirm = PasswordField('Repeat Password')


class EditUserForm(FlaskForm):
    username = StringField('username')
    name = StringField('name', validators=[Length(min=4, max=24)])
    email = StringField('email', validators=[Length(min=4, max=24), change_email])
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         CheckPasswordCorrect()
                                         ])
    new_password = PasswordField('new_password',
                                 validators=[EqualTo('confirm',
                                                     message='Passwords must match'),
                                             ])
    confirm = PasswordField('Repeat Password')


class ConfirmPassword(FlaskForm):
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         check_password
                                         ])
