import datetime
import getpass

from application import db, app
from application.flicket_admin.models.flicket_config import FlicketConfig
from application.flicket.models.flicket_models import FlicketStatus, FlicketPriority, FlicketDepartment, FlicketCategory
from application.flicket.models.flicket_user import FlicketUser, FlicketGroup
from application.flicket.scripts.hash_password import hash_password

admin = 'flicket_admin'

# configuration defaults for flicket
flicket_config = {'posts_per_page': 50,
                  'allowed_extensions': ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'],
                  'ticket_upload_folder': 'application/flicket/static/flicket_uploads'
                  }

# departments and categories defaults for flicket
depart_categories = [
    {'department': 'Design', 'category': ['Dataset', 'ECN', 'ECR', 'CATIA', 'Other']},
    {'department': 'Manufacturing', 'category': ['Process Planning', 'Tooling', 'Equipment', 'Other']},
    {'department': 'IT', 'category': ['Internet', 'Intranet', 'PC', 'Sharepoint', 'CATIA']},
    {'department': 'Quality', 'category': ['Work Instruction', 'Other']},
    {'department': 'Human Resources', 'category': ['Holidays', 'Sick Leave', 'Other']},
    {'department': 'Commercial', 'category': ['Approved Suppliers', 'Dynamics', 'Other']},

]


def set_config_defaults():
    count = FlicketConfig.query.count()
    if count > 0:
        print('Flicket Config database seems to already be populated. Check values via application.')
        return

    set_config = FlicketConfig(
        posts_per_page = flicket_config['posts_per_page'],
        allowed_extensions= ', '.join(flicket_config['allowed_extensions']),
        ticket_upload_folder=flicket_config['ticket_upload_folder'],
    )

    print('Adding config values to database.')
    db.session.add(set_config)
    db.session.commit()



def get_admin_details():
    # todo: add some password validation to prevent easy passwords being entered
    _username = admin
    match = False

    email = input("Enter flicket_admin email: ")

    while match is False:
        password1 = getpass.getpass("Enter password: ")
        password2 = getpass.getpass("Re-enter password: ")

        if password1 != password2:
            print("Passwords do not match, please try again.\n\n")
            match = False
        else:
            return _username, password1, email


def create_admin(username, password, email, silent=False):
    """ creates flicket_admin user. """
    query = FlicketUser.query.filter_by(username=username)
    if query.count() == 0:
        add_user = FlicketUser(username=username,
                               name=username,
                               password=hash_password(password),
                               email=email,
                               date_added=datetime.datetime.now())
        db.session.add(add_user)

        if silent is False:
            print("Admin user added.")


def create_announcer():
    """ creates announcer user """
    query = FlicketUser.query.filter_by(username=app.config['ANNOUNCER']['username'])
    if query.count() == 0:
        add_user = FlicketUser(username=app.config['ANNOUNCER']['username'],
                               name=app.config['ANNOUNCER']['name'],
                               password=hash_password(app.config['ANNOUNCER']['password']),
                               email=app.config['ANNOUNCER']['email'],
                               date_added=datetime.datetime.now())
        db.session.add(add_user)
        print("Announcer user added.")


def create_admin_group(silent=False):
    """ creates flicket_admin group and assigns flicket_admin to group. """
    query = FlicketGroup.query.filter_by(group_name=app.config['ADMIN_GROUP_NAME'])
    if query.count() == 0:
        add_group = FlicketGroup(group_name=app.config['ADMIN_GROUP_NAME'])
        db.session.add(add_group)
        if silent is False:
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
        if silent is False:
            print("Added flicket_admin user to flicket_admin group.")


def create_default_ticket_status():
    # set up default status levels
    sl = ['Open', 'Closed', 'In Work']
    for s in sl:
        status = FlicketStatus.query.filter_by(status=s).first()

        if not status:
            add_status = FlicketStatus(status=s)
            db.session.add(add_status)
            print('Added status level {}'.format(s))


def create_default_priority_levels(silent=False):

    """ set up default priority levels """
    pl = ['low', 'medium', 'high']
    for p in pl:
        priority = FlicketPriority.query.filter_by(priority=p).first()

        if not priority:
            add_priority = FlicketPriority(priority=p)
            db.session.add(add_priority)

            if silent is False:
                print('Added priority level {}'.format(p))


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

            if silent is False:
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


def set_email_config():
    """
    To stop mail send errors after intial set-up set the email configuration value for suppress
    send will be set to True
    :return:
    """
    query = FlicketConfig.query.first()
    if query.first().mail_server is None:
        query.mail_suppress_send = True
        db.session.commit()


if __name__ == '__main__':
    username, password, email = get_admin_details()
    set_config_defaults()
    create_admin(username=username, password=password, email=email)
    create_announcer()
    create_admin_group()
    create_default_ticket_status()
    create_default_priority_levels()
    create_default_depts()
    # commit changes to the database
    set_email_config()
    db.session.commit()
