#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import Blueprint

import os

static_folder = os.path.join(os.getcwd(), 'application/home/static')

admin_bp = Blueprint('admin_bp', __name__,
                     template_folder="../templates",
                     static_folder=static_folder,
                     static_url_path='/home/static',
                     )
