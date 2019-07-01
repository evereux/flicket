#! usr/bin/python3
# -*- coding: utf-8 -*-


from base64 import b64encode
from getpass import getpass
import json
import os

from scripts.password_valdation import PasswordStrength

config_file = 'config.json'
config_file = os.path.join(os.getcwd(), config_file)


class WriteConfigJson:

    @staticmethod
    def json_exists():
        if os.path.isfile(config_file):
            return True
        else:
            print('Config json file "{}" does not exist. Exiting application.'.format(config_file))
            exit()

    @staticmethod
    def create_file():
        """
        Primarily used for set up purposes only.
        :return:
        """

        def random_string(bytes=24):
            b = os.urandom(bytes)
            return b64encode(b).decode('utf-8')

        # Check to see if the json file already exists.
        create_file = False
        if os.path.isfile(config_file):
            overwrite = input('\n\nConfiguration json file already exists. Do you wish to overwrite? (Y/n) > ')
            if overwrite == 'Y':
                create_file = True
            else:
                exit()
        else:
            create_file = True

        if create_file is False:
            print('\n\nYou have chosen not to overwrite configuration file. Skipping json creation.')
            return

        db_username = input('Enter database username: ')
        db_password = False
        valid = False
        while valid is False:
            print(PasswordStrength.message_rules())
            validity = []
            db_password = getpass('Enter database password: ')
            password_strength = PasswordStrength(db_password)
            if password_strength.is_valid():
                validity.append(True)
            else:
                validity.append(False)
            db_password_confirm = getpass('Re-enter database password: ')
            if db_password != db_password_confirm:
                print('Passwords do not match, please try again.\n\n')
                validity.append(False)
            else:
                validity.append(True)

            if all(validity):
                valid = True

        db_url = input('Enter database url (don\'t include port). If running locally this would be localhost: ')
        db_port = input('Enter database port: ')
        db_name = input('Enter database name: ')

        secret_key = random_string()
        notification_user_password = random_string()

        config_values = {
            'db_username': db_username,
            'db_password': db_password,
            'db_url': db_url,
            'db_port': db_port,
            'db_name': db_name,
            'SECRET_KEY': secret_key,
            'NOTIFICATION_USER_PASSWORD': notification_user_password
        }

        # write json file
        with open(config_file, 'w') as f:
            print('Writing config file to {}'.format(config_file))
            json.dump(config_values, f)


if __name__ == '__main__':
    WriteConfigJson.create_file()
