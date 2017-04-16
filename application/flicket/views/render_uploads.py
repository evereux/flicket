#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os
from flask import send_from_directory
from flask_login import login_required

from . import flicket_bp
from application import app


# return images
@flicket_bp.route(app.config['WEBHOME'] + 'flicket_uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def view_ticket_uploads(filename):
    path = os.path.join(os.getcwd(), app.config['ticket_upload_folder'])
    return send_from_directory(path, filename)
