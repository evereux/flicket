#! python3

import datetime
from random import randint

from application.models import User
from random_words import LoremIpsum, RandomWords, RandomNicknames, RandomEmails

from application import db
from application.flicket.models.flicket_models import FlicketTicket, \
    FlicketStatus, \
    FlicketPriority, \
    FlicketCategory, \
    FlicketPost
from application.flicket.scripts import hash_password

num_topics = 5000
num_replies = 25
num_users = 1000

rn = RandomNicknames()
re = RandomEmails()


# get a list of users and return a random one
def get_random_user():
    user = User.query
    id = randint(1, user.count())

    return User.query.filter_by(id=id).first()


def get_random_status():
    status = FlicketStatus.query
    id = randint(1, status.count())

    return FlicketStatus.query.filter_by(id=id).first()


def get_random_priority():
    priority = FlicketPriority.query
    id = randint(1, priority.count())

    return FlicketPriority.query.filter_by(id=id).first()


def get_random_category():
    category = FlicketCategory.query
    id = randint(1, category.count())

    return FlicketCategory.query.filter_by(id=id).first()


def get_random_sentance(number=10):
    li = LoremIpsum()
    return li.get_sentences(number)


def get_random_words():
    words = RandomWords().random_words(count=2)
    title = ''
    for w in words:
        title = title + ' ' + w
    return title


def create_ticket_reply(new_ticket):
    new_reply = FlicketPost(
        ticket=new_ticket,
        content=get_random_sentance(),
        user=get_random_user(),
        date_added=datetime.datetime.now()
    )

    db.session.add(new_reply)


def create_random_user():
    nicknames = rn.random_nicks(gender='u', count=2)
    email = re.randomMails()[0]
    password = rn.random_nick(gender='u')

    username = '{}{}'.format(nicknames[0], nicknames[1]).lower()
    name = '{} {}'.format(nicknames[0], nicknames[1])

    return username, name, password, email


def user_creation():
    # count how many users are in database. if it is already populated don't add any more.
    user_count = User.query.count()
    if user_count == num_users:
        print('Number of users already satisfied.')
        return

    for i in range(user_count, num_users):

        username, name, password, email = create_random_user()

        # check username doesn't already exist
        query = User.query.filter_by(username=username).first()

        if not query:
            new_user = User(
                username=username,
                name=name,
                password=hash_password(password),
                email=email,
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

        new_ticket = FlicketTicket(
            title=get_random_words(),
            content=get_random_sentance(),
            user=get_random_user(),
            date_added=datetime.datetime.now(),
            current_status=get_random_status(),
            ticket_priority=get_random_priority(),
            category=get_random_category(),
            assigned=get_random_user()
        )

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
