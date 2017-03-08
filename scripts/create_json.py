#! usr/bin/python3
# -*- coding: utf8 -*-

import os
from getpass import getpass
import json

config_file = 'config.json'
config_file = os.path.join(os.getcwd(), config_file)


class WriteConfigJson(object):

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

        # Check to see if the json file already exists.
        create_file = False
        if os.path.isfile(config_file):
            overwrite = input('\n\nConfiguration json file already exists. Do you wish to overwrite? (Y/n) > ')
            if overwrite != 'Y':
                create_file = True
        else:
            create_file = True

        if create_file is False:
            print('\n\nYou have chosen not to overwrite configuration file. Skipping json creation.')
            return

        db_username = input('Enter database username: ')
        db_password = False
        match = False
        while match is False:
            db_password = getpass('Enter database password: ')
            db_password_confirm = getpass('Re-enter database password: ')
            if db_password != db_password_confirm:
                print('Passwords do not match, please try again.\n\n')
                match = False
            else:
                match = True

        db_url = input('Enter database url (don\'t include port). If running locally this would be local host: ')
        db_port = input('Enter database port: ')
        db_name = input('Enter database name: ')

        config_values = {
            'db_username': db_username,
            'db_password': db_password,
            'db_url': db_url,
            'db_port': db_port,
            'db_name': db_name
        }

        # write json file
        with open(config_file, 'w') as f:
            print('Writing config file to {}'.format(config_file))
            json.dump(config_values, f)

if __name__ == '__main__':

    WriteConfigJson.create_file()
