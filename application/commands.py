#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime
import json
from getpass import getpass
import os
import time

from sqlalchemy import or_

from scripts.create_json import WriteConfigJson
from application import db, app
from application.flicket_admin.models.flicket_config import FlicketConfig
from application.flicket.models.flicket_models import FlicketCategory
from application.flicket.models.flicket_models import FlicketDepartment
from application.flicket.models.flicket_models import FlicketPriority
from application.flicket.models.flicket_models import FlicketStatus
from application.flicket.models.flicket_models import FlicketTicket
from application.flicket.models.flicket_user import FlicketGroup
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.email import FlicketMail
from application.flicket.scripts.flicket_user_details import FlicketUserDetails
from application.flicket.scripts.hash_password import hash_password

admin = 'admin'

# configuration defaults for flicket
flicket_config = {'posts_per_page': 50,
                  'allowed_extensions': ['txt', 'log', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'msg', 'doc', 'docx', 'ppt',
                                         'pptx', 'xls', 'xlsx'],
                  'ticket_upload_folder': 'application/flicket/static/flicket_uploads',
                  'avatar_upload_folder': 'application/flicket/static/flicket_avatars',
                  }

# departments and categories defaults for flicket
depart_categories = [
    {'department': 'Design', 'category': ['Dataset', 'ECN', 'ECR', 'Other']},
    {'department': 'Manufacturing', 'category': ['Process Planning', 'Tooling', 'Equipment', 'Other']},
    {'department': 'IT', 'category': ['Internet', 'Intranet', 'Other']},
    {'department': 'Quality', 'category': ['Procedures', 'Manuals', 'Other']},
    {'department': 'Human Resources', 'category': ['Holidays', 'Sick Leave', 'Other']},
    {'department': 'Commercial', 'category': ['Approved Suppliers', 'Other']},

]

json_user_file = 'users.json'


class JsonUser:

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.name = name
        self.password = password


def create_admin(username, password, email, job_title, silent=False):
    """ creates flicket_admin user. """

    query = FlicketUser.query.filter_by(username=username)
    if query.count() == 0:
        add_user = FlicketUser(username=username,
                               name=username,
                               password=hash_password(password),
                               email=email,
                               job_title=job_title,
                               date_added=datetime.datetime.now())
        db.session.add(add_user)

        if not silent:
            print('Admin user added.')
    else:
        print('Admin user is already added.')


def create_admin_group(silent=False):
    """ creates flicket_admin and super_user group and assigns flicket_admin to group admin. """

    query = FlicketGroup.query.filter_by(group_name=app.config['ADMIN_GROUP_NAME'])
    if query.count() == 0:
        add_group = FlicketGroup(group_name=app.config['ADMIN_GROUP_NAME'])
        db.session.add(add_group)
        if not silent:
            print("Admin group added")

    user = FlicketUser.query.filter_by(username=admin).first()
    group = FlicketGroup.query.filter_by(group_name=app.config['ADMIN_GROUP_NAME']).first()
    in_group = False
    # see if user flicket_admin is already in flicket_admin group.
    for g in group.users:
        if g.username == admin:
            in_group = True
            break
    if not in_group:
        group.users.append(user)
        if not silent:
            print("Added flicket_admin user to flicket_admin group.")

    #  create the super_user group
    query = FlicketGroup.query.filter_by(group_name=app.config['SUPER_USER_GROUP_NAME'])
    if query.count() == 0:
        add_group = FlicketGroup(group_name=app.config['SUPER_USER_GROUP_NAME'])
        db.session.add(add_group)
        if not silent:
            print("super_user group added")


def create_default_depts(silent=False):
    """ creates default departments and categories. """

    for d in depart_categories:

        department = d['department']
        categories = d['category']

        query = FlicketDepartment.query.filter_by(department=department).first()
        if not query:
            add_department = FlicketDepartment(
                department=department
            )
            db.session.add(add_department)

            if not silent:
                print("department {} added.".format(department))

            for c in categories:
                query = FlicketCategory.query.filter_by(category=c).first()
                if not query:
                    add_category = FlicketCategory(
                        category=c,
                        department=add_department
                    )
                    db.session.add(add_category)

                    if silent is False:
                        print("category {} added.".format(c))


def create_default_priority_levels(silent=False):
    """ set up default priority levels """

    pl = ['low', 'medium', 'high']
    for p in pl:
        priority = FlicketPriority.query.filter_by(priority=p).first()

        if not priority:
            add_priority = FlicketPriority(priority=p)
            db.session.add(add_priority)

            if not silent:
                print('Added priority level {}'.format(p))


def create_default_ticket_status(silent=False):
    """ set up default status levels """

    sl = ['Open', 'Closed', 'In Work', 'Awaiting Information']
    for s in sl:
        status = FlicketStatus.query.filter_by(status=s).first()

        if not status:
            add_status = FlicketStatus(status=s)
            db.session.add(add_status)
            if not silent:
                print('Added status level {}'.format(s))


def create_default_priority_levels(silent=False):
    """ set up default priority levels """

    pl = ['low', 'medium', 'high']
    for p in pl:
        priority = FlicketPriority.query.filter_by(priority=p).first()

        if not priority:
            add_priority = FlicketPriority(priority=p)
            db.session.add(add_priority)

            if not silent:
                print('Added priority level {}'.format(p))


def create_notifier():
    """ creates user for notifications """

    query = FlicketUser.query.filter_by(username=app.config['NOTIFICATION']['username'])
    if query.count() == 0:
        add_user = FlicketUser(username=app.config['NOTIFICATION']['username'],
                               name=app.config['NOTIFICATION']['name'],
                               password=hash_password(app.config['NOTIFICATION']['password']),
                               email=app.config['NOTIFICATION']['email'],
                               date_added=datetime.datetime.now())
        db.session.add(add_user)
        print("Notification user added.")
    else:
        print('Notification user already added.')


def get_admin_details():
    # todo: add some password validation to prevent easy passwords being entered
    _username = admin
    match = False

    email = input("Enter admin email: ")

    while match is False:
        password1 = getpass("Enter password: ")
        password2 = getpass("Re-enter password: ")

        if password1 != password2:
            print("Passwords do not match, please try again.\n\n")
            match = False
        else:
            return _username, password1, email


def set_db_config_defaults(silent=False):
    print('Please enter site base url including port. For example this would be "http://192.168.1.1:8000".')
    base_url = input('Base url> ')

    count = FlicketConfig.query.count()
    if count > 0:
        if not silent:
            print('Flicket Config database seems to already be populated. Check values via application.')
        return

    set_config = FlicketConfig(
        posts_per_page=flicket_config['posts_per_page'],
        allowed_extensions=', '.join(flicket_config['allowed_extensions']),
        ticket_upload_folder=flicket_config['ticket_upload_folder'],
        avatar_upload_folder=flicket_config['avatar_upload_folder'],
        base_url=base_url,
        application_title='Flicket',
        mail_max_emails=10,
        mail_port=465
    )

    if not silent:
        print('Adding config values to database.')

    db.session.add(set_config)
    db.session.commit()


def set_email_config(silent=False):
    """
    To stop mail send errors after initial set-up set the email configuration value for suppress
    send will be set to True
    :return:
    """

    query = FlicketConfig.query.first()
    if query.mail_server is None:
        query.mail_debug = True
        query.mail_suppress_send = True
        db.session.commit()
        if not silent:
            print(
                'Setting email settings to suppress sending. Change values via administration panel with in '
                'Flicket.')


def register_clicks(app):
    """

    """

    @app.cli.command('run-set-up', help='Initialise database defaults.')
    def run_set_up():
        WriteConfigJson().json_exists()
        username, password, email = get_admin_details()
        set_db_config_defaults()
        set_email_config()
        create_admin(username=username, password=password, email=email, job_title='admin')
        create_notifier()
        create_admin_group()
        create_default_ticket_status()
        create_default_priority_levels()
        create_default_depts()
        # commit changes to the database
        db.session.commit()

    @app.cli.command('export-users-to-json', help='Export all users from database to json file.')
    def export_users_to_json():

        # query database.
        users = FlicketUser.query.all()
        output_list = []

        for u in users:
            loop_dict = dict()
            loop_dict['username'] = u.username
            loop_dict['name'] = u.name
            loop_dict['email'] = u.email
            loop_dict['password'] = u.password.decode('utf-8')
            output_list.append(loop_dict)

        # check existence of json file.
        if os.path.isfile(json_user_file):

            while True:
                over_write = input('json user file already exists. Over write? (Y/n)> ')
                if over_write == 'Y':
                    return False
                else:
                    print('You have opted to not over write. Exiting ....')
                    exit()

        file_text = json.dumps(output_list)

        with open(json_user_file, 'w') as f:
            f.write(file_text)

    @app.cli.command('import-users-from-json', help='Export all users from database to json file.')
    def import_users_from_json():
        # check if file exists
        if not os.path.isfile(json_user_file):
            print('Could not find json file "{}". Exiting ....'.format(json_user_file))
            exit()

        # read json file
        with open(json_user_file) as data_file:
            json_users = json.load(data_file)

        # check formatting of json file
        valid_json_fields = ['username', 'name', 'email', 'password']
        for user in json_users:
            if not all(f in user for f in valid_json_fields):
                print('json file not formatted correctly. Exiting.')
                exit()

        # add users to database.
        for user in json_users:

            # encode password to bytes
            password = str.encode(user['password'])

            # create json_user object
            json_user = JsonUser(user['username'], user['name'], user['email'], password)

            # check tht user doesn't already exist.
            existing_user = FlicketUser.query.filter_by(email=json_user.email)
            if existing_user.count() > 0:
                print('User {} {} already exists in the database.'.format(json_user.name, json_user.email))
                continue

            # add the user
            print('Adding the user {} {} to the database.'.format(json_user.name, json_user.email))
            new_user = FlicketUser(username=json_user.username, name=json_user.name, email=json_user.email,
                                   password=json_user.password, date_added=datetime.datetime.now())
            db.session.add(new_user)
            db.session.commit()

    @app.cli.command('update-total-post-count', help='Update all users total post count. Use when upgrading from 1.4.')
    def update_total_post_count():

        print('!!! Warning !!!!')
        print('This script should not be run whilst the server is running.')
        print('Calculated totals could change.')
        input('Enter to continue.')
        users = FlicketUser.query.all()
        all_good = True
        for user in users:
            user_details_total = FlicketUserDetails(user).num_posts
            if user_details_total != user.total_posts:
                print("{} had a calculated post count of {} and a table count of {}. This will be updated.".format(
                    user.username, user_details_total, user.total_posts))
                user.total_posts = user_details_total
                db.session.commit()
                all_good = False
        if all_good:
            print('No updates were required.')
        else:
            print('Updates were made.')

    @app.cli.command('update-total-user_assigned',
                     help='Update all users total post count. Use when upgrading from 1.4.')
    def update_total_user_assigned():

        print('!!! Warning !!!!')
        print('This script should not be run whilst the server is running.')
        print('Calculated totals could change.')
        input('Enter to continue.')

        users = FlicketUser.query.all()
        all_good = True
        for user in users:
            user_details_total = FlicketUserDetails(user).num_assigned
            if user_details_total != user.total_assigned:
                print("{} had a calculated assigned count of {} and a table count of {}. This will be updated.".format(
                    user.username, user_details_total, user.total_posts))
                user.total_assigned = user_details_total
                db.session.commit()
                all_good = False
        if all_good:
            print('No updates were required.')
        else:
            print('Updates were made.')

    @app.cli.command('email-outstanding-tickets',
                     help='Update all users total post count. Use when upgrading from 1.4.')
    def email_outstanding_tickets():
        # find all users
        users = FlicketUser.query.all()
        for user in users:
            # that have created a ticket or have a ticket assigned to them.
            tickets = FlicketTicket.query.filter(or_(
                FlicketTicket.user == user,
                FlicketTicket.assigned == user,
            )).filter(
                FlicketTicket.status_id != 2)

            if tickets.count() > 0:
                mail = FlicketMail()
                mail.tickets_not_closed(user, tickets)
                time.sleep(10)
