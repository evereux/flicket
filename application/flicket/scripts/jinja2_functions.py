#! usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

import markdown
from markupsafe import Markup


def now_year():
    return datetime.datetime.now().strftime('%Y')

def render_markdown(text):
    if not text:
        return ""
    # You can add extensions like 'fenced_code' or 'tables' here
    return Markup(markdown.markdown(text, extensions=['fenced_code', 'tables']))