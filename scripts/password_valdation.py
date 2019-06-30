#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import string

password_length = 8


class PasswordStrength:

    def __init__(self, password, special_characters=False):
        """
        Checks validity of password.
        :param special_characters:
        :return:
        """
        self.password = password
        # currently not supported
        # todo: added special characters requirements
        self.special_characters = special_characters

    def is_valid(self):
        minimum_length = False
        has_digits = False
        has_uppercase = False
        has_lowercase = False

        if password_length >= password_length:
            minimum_length = True

        for digit in string.digits:
            if digit in self.password:
                has_digits = True

        for char in string.ascii_uppercase:
            if char in self.password:
                has_uppercase = True

        for char in string.ascii_lowercase:
            if char in self.password:
                has_lowercase = True

        if all([minimum_length, has_digits, has_uppercase, has_lowercase]):
            return True
        else:
            return False

    @staticmethod
    def message_rules():
        return ("Password must: \n"
                "  * be a minimum of {} characters long.\n"
                "  * contain numbers and letters.\n"
                "  * contain one lowercase and one uppercase letter."
                ).format(password_length)

    def __repr__(self):
        return "<PasswordValidator>"
