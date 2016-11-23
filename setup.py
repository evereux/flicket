import datetime
import getpass

from application import db, app
from application.admin.models.user import User, Group
from application.flicket.models.flicket_models import FlicketStatus, FlicketPriority, FlicketDepartment, FlicketCategory
from application.flicket.scripts.hash_password import hash_password

ADMIN = 'admin'

# departments and categories defaults for flicket
departcategories = [
    {'department': 'Design', 'category': ['Dataset', 'ECN', 'ECR', 'CATIA', 'Other']},
    {'department': 'Manufacturing', 'category': ['Process Planning', 'Tooling', 'Equipment', 'Other']},
    {'department': 'IT', 'category': ['Internet', 'Intranet', 'PC', 'Sharepoint', 'CATIA']},
    {'department': 'Quality', 'category': ['Work Instruction', 'Other']},
    {'department': 'Human Resources', 'category': ['Holidays', 'Sick Leave', 'Other']},
    {'department': 'Commercial', 'category': ['Approved Suppliers', 'Dynamics', 'Other']},

]


def get_admin_details():
    # todo: add some password validation to prevent easy passwords being
    # entered
    _username = ADMIN
    match = False

    email = input("Enter admin email: ")

    while match is False:
        password1 = getpass.getpass("Enter password: ")
        password2 = getpass.getpass("Re-enter password: ")

        if password1 != password2:
            print("Passwords do not match, please try again.\n\n")
            match = False
        else:
            match = True
            return _username, password1, email


def create_admin(username, password, email, silent=False):
    """ creates admin user. """
    query = User.query.filter_by(username=username)
    if query.count() == 0:
        add_user = User(username=username,
                        name=username,
                        password=hash_password(password),
                        email=email,
                        date_added=datetime.datetime.now())
        db.session.add(add_user)

        if silent is False:
            print("Admin user added.")


def create_announcer():
    """ cretes announcer user """
    query = User.query.filter_by(username=app.config['ANNOUNCER']['username'])
    if query.count() == 0:
        add_user = User(username=app.config['ANNOUNCER']['username'],
                        name=app.config['ANNOUNCER']['name'],
                        password=hash_password(app.config['ANNOUNCER']['password']),
                        email=app.config['ANNOUNCER']['email'],
                        date_added=datetime.datetime.now())
        db.session.add(add_user)
        print("Announcer user added.")



def for_testing_only(silent=False):
    """ adds some generic users. this is for testing only! """
    users = [
        ('paul', 'paul wauly', '12345', 'evereux1@gmail.com'),
        ('bill', 'billy bob', '12345', 'evereux2@gmail.com'),
        ('nicola', 'nicola pikola', '12345', 'evereux3@gmail.com'),
        ('jenny', 'jenny wenny', '12345', 'evereux4@gmail.com'),
        ('ryan', 'ryan newby', '12345', 'evereux6@gmail.com'),
        ('luke', 'luke newby', '12345', 'evereux7@gmail.com'),
    ]
    for u in users:

        user = User.query.filter_by(username=u[0]).first()
        if not user:
            add_user = User(
                username=u[0],
                name=u[1],
                password=hash_password(u[2]),
                email=u[3],
                date_added=datetime.datetime.now()
            )
            db.session.add(add_user)

            if silent is False:
                print("user {} added.".format(u[1]))



def create_admin_group(silent=False):
    """ creates admin group and assigns admin to group. """
    query = Group.query.filter_by(group_name=app.config['ADMIN_GROUP_NAME'])
    if query.count() == 0:
        add_group = Group(group_name=app.config['ADMIN_GROUP_NAME'])
        db.session.add(add_group)
        if silent is False:
            print("Admin group added")

    user = User.query.filter_by(username=ADMIN).first()
    group = Group.query.filter_by(group_name=app.config['ADMIN_GROUP_NAME']).first()
    in_group = False
    # see if user admin is already in admin group.
    for g in group.users:
        if g.username == ADMIN:
            in_group = True
            break
    if not in_group:
        group.users.append(user)
        if silent is False:
            print("Added admin user to admin group.")


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
    for d in departcategories:

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


if __name__ == '__main__':
    username, password, email = get_admin_details()

    create_admin(username=username, password=password, email=email)
    create_announcer()
    for_testing_only()  # todo: remove this!
    create_admin_group()
    create_default_ticket_status()
    create_default_priority_levels()
    create_default_depts()
    # commit changes to the database
    db.session.commit()
