#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from threading import Thread

def async(f):
    """
    Threading function blatantly copied from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
    :param f:
    :return:
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper