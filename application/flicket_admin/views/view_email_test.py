#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash
from flask import Markup
from flask import url_for
from flask import render_template
from flask_babel import gettext
from flask_login import login_required

from application import app
from application.flicket_admin.forms.form_config import EmailTest
from application.flicket.scripts.email import FlicketMail

from . import admin_bp
from .view_admin import admin_permission


# Configuration view
@admin_bp.route(app.config['ADMINHOME'] + 'test_email/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def email_test():
    form = EmailTest()

    if form.validate_on_submit():
        # send email notification
        mail = FlicketMail()
        mail.test_email([form.email_address.data])
        flash(Markup(gettext(
            'Flicket has tried to send an email to the address you entered. Please check your inbox. If no email has '
            'arrived please double check the <a href="{}{url_for("admin_bp.config")}">config</a>'
            ' settings.'.format(app.config["base_url"]))),
            category='warning')

    return render_template('admin_email_test.html',
                           title='Send Email Test',
                           form=form)
