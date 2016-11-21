import re
import bcrypt

from application.models import User


def check_password_format(password):
    """
    Checks that the password adheres to the rules defined by this function.
    Passwords must contain upper and lower case letters.
    :param password:
    :return: True if ok
    """
    if not ((any(s.isupper() for s in password)) and (any(s.islower() for s in password))):
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

    query = User.query.filter_by(username=username)
    if query.count() == 1:
        return True
    return False


def is_registered_password_correct(username, password):
    """
    :param username:
    :param password:
    :return: True if password is correct
    """

    user = User.query.filter_by(username=username).first()
    hashed = user.password
    password = password.encode('utf-8')

    if bcrypt.hashpw(password, hashed) == hashed:
        return True
    return False
