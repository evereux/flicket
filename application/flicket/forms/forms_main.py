#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import bcrypt
from flask import g
from flask_wtf import FlaskForm
from wtforms import (PasswordField,
                     StringField,
                     FileField)
from wtforms.validators import (DataRequired,
                                Length,
                                EqualTo)

from application.flicket.models.flicket_user import (FlicketUser,
                                                     user_field_size)

from application.flicket.scripts.functions_login import check_email_format


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


def check_password_formatting(form, field):
    """
    Check formatting of password.
    :param field:
    :return True / False:
    """
    ok = True
    min = 6
    if len(field.data) < min:
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
    result = FlicketUser.query.filter_by(username=g.user.username).first()
    if bcrypt.hashpw(form.password.data.encode('utf-8'), result.password) != result.password:
        field.errors.append('Entered password is incorrect.')
        return False
    return ok


def check_email(form, field):
    ok = True
    if not check_email_format(field.data):
        field.errors.append('Please enter a valid email address.')
        ok = False
    result = FlicketUser.query.filter_by(email=form.email.data).count()
    if result > 0:
        field.errors.append('A user with this email address has already registered.')
        ok = False

    return ok


def change_email(form, field):
    """
    Ensure the form email matches the users email.
    :param form:
    :param field:
    :return:
    """

    if form.email.data == g.user.email:
        return True
    else:
        return False


class CheckPasswordCorrect:
    """
    Check that the entered password matches that in the database.
    """
    def __call__(self, form, field):
        self.username = form.username.data
        self.password = form.password.data
        self.password = self.password.encode('utf-8')
        ok = True
        user = FlicketUser.query.filter_by(username=form.username.data).first()
        # hashed = user.password
        if user and not bcrypt.hashpw(self.password, user.password) == user.password:
            field.errors.append('Your username and password do not match those in the database.')
            ok = False

        return ok


class EditUserForm(FlaskForm):
    username = StringField('username')
    name = StringField('name', validators=[Length(min=user_field_size['name_min'], max=user_field_size['name_max'])])
    email = StringField('email', validators=[Length(min=user_field_size['email_min'], max=user_field_size['email_max']), change_email])
    avatar = FileField('avatar')
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         CheckPasswordCorrect(),
                                         Length(min=user_field_size['password_min'], max=user_field_size['password_max'])])
    new_password = PasswordField('new_password',
                                 validators=[EqualTo('confirm',
                                                     message='Passwords must match'),
                                             ])
    confirm = PasswordField('Repeat Password')
    job_title = StringField('job_title', validators=[Length(max=user_field_size['job_title'])])


class ConfirmPassword(FlaskForm):
    password = PasswordField('password',
                             validators=[DataRequired(),
                                         check_password
                                         ])
