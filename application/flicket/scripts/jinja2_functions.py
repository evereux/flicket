#! usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template

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

    return render_template('flicket_post.html', ticket=ticket, post=post, content=content, replies=replies, loop=loop, page=page)
