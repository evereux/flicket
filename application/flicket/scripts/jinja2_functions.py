#! usr/bin/python3
# -*- coding: utf-8 -*-

import datetime

from flask import render_template


def now_year():
    return datetime.datetime.now().strftime('%Y')
