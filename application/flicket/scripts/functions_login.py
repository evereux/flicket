#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import re

import bcrypt
from flask_babel import gettext

from application.flicket.models.flicket_user import FlicketUser

password_requirements = gettext('Passwords shall adhere to the following:<br>'
                                '1. Be a minimum of 8 characters.<br>'
                                '2. Contain at least one digit.<br>'
                                '3. Contain at least one upper and lower case character.<br>'
                                '4. Not contain your username.<br>')


def check_password_format(password, username, email):
    """
    Checks that the password adheres to the rules defined by this function.
    See `password_requirements`.
    :param password:
    :param username:
    :param email:
    :return: True if ok
    """
    if not ((any(s.isupper() for s in password)) and (any(s.islower() for s in password))):
        return False
    if len(password) < 8:
        return False
    if not any([c.isdigit() for c in password]):
        return False
    if username in password:
        return False
    if email in password:
        return False

    return True


def check_email_format(email):
    """
    Checks that the email adheres to the rules defined by this function
    :param email:
    :return: True if ok
    """
    email_regex = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))')
    if not email_regex.match(email):
        return False
    return True


def is_user_registered(username):
    """
    is the entered user registered on website?
    :param username:
    :return: True if registered
    """

    query = FlicketUser.query.filter_by(username=username)
    if query.count() == 1:
        return True
    return False


def is_registered_password_correct(username, password):
    """
    :param username:
    :param password:
    :return: True if password is correct
    """

    user = FlicketUser.query.filter_by(username=username).first()
    hashed = user.password
    password = password.encode('utf-8')

    if bcrypt.hashpw(password, hashed) == hashed:
        return True
    return False
