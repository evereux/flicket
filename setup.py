#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime
from getpass import getpass

from flask_script import Command

from scripts.create_json import WriteConfigJson
from application import db, app
from application.flicket_admin.models.flicket_config import FlicketConfig
from application.flicket.models.flicket_models import FlicketStatus, FlicketPriority, FlicketDepartment, FlicketCategory
from application.flicket.models.flicket_user import FlicketUser, FlicketGroup
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


class RunSetUP(Command):

    def run(self):
        WriteConfigJson().json_exists()
        username, password, email = self.get_admin_details()
        self.set_db_config_defaults()
        self.set_email_config()
        self.create_admin(username=username, password=password, email=email, job_title='admin')
        self.create_notifier()
        self.create_admin_group()
        self.create_default_ticket_status()
        self.create_default_priority_levels()
        self.create_default_depts()
        # commit changes to the database
        db.session.commit()

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    # noinspection PyArgumentList
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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


class TestingSetUp:

    @staticmethod
    def set_db_config_defaults_testing(silent=False):
        """
        Set config defaults. Only used for unit testing
        :param silent:
        :return:
        """

        set_config = FlicketConfig(
            posts_per_page=10,
            allowed_extensions='txt,  jpg',
            ticket_upload_folder='tmp/uploads',
            base_url='',
            mail_debug=True,
            mail_suppress_send=True,
        )

        if not silent:
            print('Adding config values to database.')

        db.session.add(set_config)
        db.session.commit()
