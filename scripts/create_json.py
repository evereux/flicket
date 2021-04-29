#! usr/bin/python3
# -*- coding: utf-8 -*-


from base64 import b64encode
from getpass import getpass
import json
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

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

        def random_string(bytes_=24):
            b = os.urandom(bytes_)
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

        db_type = False
        while db_type is False:
            select_type = input('Please select database type:\n'
                                '1 = SQLite\n'
                                '2 = PostreSQL\n'
                                '3 = MySQL.\n'
                                '> ')
            if select_type == "1" or select_type == "2" or select_type == "3":
                db_type = int(select_type)

        db_username = None
        db_password = None
        db_url = None
        db_port = None

        if db_type != 1:

            db_username = input('Enter database username: ')

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

        db_name = input('For SQLite this should be the filename e.g. flicket.db \n'
                        'Enter database name: ')

        secret_key = random_string()
        notification_user_password = random_string()

        config_values = {
            'db_type': db_type,
            'db_driver': None,
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


def check_db_connection(sqlalchemy_database_uri):
    """

    :param sqlalchemy_database_uri:
    :return: 
    """

    base_error_message = f'There was a problem connecting to the database {sqlalchemy_database_uri}. Please check your config.json file.'

    try:
        engine = create_engine(sqlalchemy_database_uri)
        engine.connect()
    except ValueError:
        raise Exception(base_error_message)
    except OperationalError:
        raise Exception(base_error_message)


if __name__ == '__main__':
    WriteConfigJson.create_file()
