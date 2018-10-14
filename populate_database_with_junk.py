#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script populates the flicket database with randomly generated text.
Run calling python populate_database_with_junk.py.
"""

import datetime
from random import randint

from mimesis import Person, Text

from application import db
from application.flicket.models.flicket_models import FlicketTicket, \
    FlicketStatus, \
    FlicketPriority, \
    FlicketCategory, \
    FlicketPost, \
    field_size
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.hash_password import hash_password
from setup import admin

num_topics = 100500
num_replies = 100
num_users = 120

# rn = RandomNicknames()

# Check to see if set-up has been run.
query = FlicketUser.query.filter_by(username=admin)
if query.count() != 1:
    print('Setup has not yet been run! You should do `python manage.py run_set_up`.')
    exit()

mismatch = True
while mismatch is True:
    print('When population with junk users will be added with <your_email_usersname>+<random_username>@<email_domain>.')
    base_email = input('Please enter your email for testing > ')
    base_email_confirm = input('Please confirm your email > ')
    if base_email == base_email_confirm:
        mismatch = False
    else:
        print('Your email address did not match. Please try again.')


# get a list of users and return a random one
def get_random_user():
    user = FlicketUser.query
    id_ = randint(1, user.count())

    return FlicketUser.query.filter_by(id=id_).first()


def get_random_status():
    status = FlicketStatus.query
    id_ = randint(1, status.count())

    return FlicketStatus.query.filter_by(id=id_).first()


def get_random_priority():
    priority = FlicketPriority.query
    id_ = randint(1, priority.count())

    return FlicketPriority.query.filter_by(id=id_).first()


def get_random_category():
    category = FlicketCategory.query
    id_ = randint(1, category.count())

    return FlicketCategory.query.filter_by(id=id_).first()


def create_ticket_reply(new_ticket):
    t = Text()

    new_reply = FlicketPost(
        ticket=new_ticket,
        content=t.text(randint(3, 15)),
        user=get_random_user(),
        date_added=datetime.datetime.now()
    )

    new_reply.user.total_posts += 1

    db.session.add(new_reply)


def create_random_user():
    person = Person('en')
    name = person.full_name()
    username = "{}_{}".format(name.split(' ')[0], name.split(' ')[1])
    password = person.password()

    return username, name, password


def user_creation():
    # count how many users are in database. if it is already populated don't add any more.
    user_count = FlicketUser.query.count()
    if user_count == num_users:
        print('Number of users already satisfied.')
        return

    for i in range(user_count, num_users):

        username, name, password = create_random_user()

        # check username doesn't already exist
        query_ = FlicketUser.query.filter_by(username=username).first()

        first, last = base_email.split('@')

        if not query_:
            new_user = FlicketUser(
                username=username,
                name=name,
                password=hash_password(password),
                email='{}+{}@{}'.format(first, username, last),
                date_added=datetime.datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()

            print('#{} Added new user {}'.format(new_user.id, username.ljust(25)), end="\r")
    print("")


def topic_creation():
    # if the number of topics is already satisfied don't add any more.
    topic_count = FlicketTicket.query.count()
    if topic_count == num_topics:
        print('Topic number already satisfied')
        return

    for i in range(topic_count, num_topics):

        t = Text()

        new_ticket = FlicketTicket(
            title=t.title()[0:field_size['title_max_length']],
            content=t.text(randint(3, 15)),
            user=get_random_user(),
            date_added=datetime.datetime.now(),
            current_status=get_random_status(),
            ticket_priority=get_random_priority(),
            category=get_random_category(),
            assigned=get_random_user()
        )

        new_ticket.user.total_posts += 1

        db.session.add(new_ticket)
        mess_1 = "#{}: ticket ....".format(i)
        print(mess_1, end="\r")

        replies = randint(0, num_replies)

        for ii in range(0, replies):
            create_ticket_reply(new_ticket)
            mess_2 = mess_1 + "adding replies ... # {}".format(ii)
            print(mess_2, end="\r")

        db.session.commit()


if __name__ == '__main__':
    user_creation()
    topic_creation()
