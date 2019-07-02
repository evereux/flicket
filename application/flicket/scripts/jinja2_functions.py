#! usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

from flask import render_template

from markdown import markdown


def display_post_box(ticket=None, post=None, replies=None, loop=None, page=None):
    """
    :param ticket: object containing ticket information
    :param post: 
    :param replies:
    :param loop: 
    :param page: 
    :return: 
    """

    if post is None:
        content = ticket
    else:
        content = post

    return render_template('flicket_post.html', ticket=ticket, post=post, content=content, replies=replies, loop=loop,
                           page=page)


def show_markdown(text):
    """
    Function to convert text to markdown.
    :param text:
    :return:
    """
    html = markdown(text, safemode="escape")

    return html


def now_year():
    return datetime.datetime.now().strftime('%Y')
