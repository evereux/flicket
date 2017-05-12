#! usr/bin/python3
# -*- coding: utf-8 -*-

from flask import render_template

def display_post_box(flicket_post, replies=None, loop=None, page=None):
    """
    :param flicket_post: object containing post information. can be ticket question or replies.
    :return: 
    """

    return render_template('flicket_post.html', flicket_post=flicket_post, replies=replies, loop=loop, page=page)
