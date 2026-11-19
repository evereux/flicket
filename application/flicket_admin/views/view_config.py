#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import os

from flask import (flash,
                   redirect,
                   render_template,
                   request,
                   url_for)
from flask_babel import gettext
from flask_login import login_required

from application import app, db
from application.flicket.scripts.flicket_upload import UploadFile
from application.flicket_admin.forms.form_config import ConfigForm
from application.flicket_admin.models.flicket_config import FlicketConfig

from . import admin_bp
from .view_admin import admin_permission


# Configuration view
@admin_bp.route(app.config['ADMINHOME'] + 'config/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def config():
    form = ConfigForm()

    config_details = FlicketConfig.query.first()

    if form.validate_on_submit():

        config_details.mail_server = form.mail_server.data
        config_details.mail_port = form.mail_port.data
        config_details.mail_use_tls = form.mail_use_tls.data or False
        config_details.mail_use_ssl = form.mail_use_ssl.data or False
        config_details.mail_debug = form.mail_debug.data or False
        config_details.mail_username = form.mail_username.data

        config_details.mail_default_sender = form.mail_default_sender.data
        config_details.mail_max_emails = form.mail_max_emails.data
        config_details.mail_suppress_send = form.mail_suppress_send.data or False
        config_details.mail_ascii_attachments = form.mail_ascii_attachments.data or False

        config_details.application_title = form.application_title.data
        config_details.branding_company_name = form.branding_company_name.data
        config_details.branding_phone = form.branding_phone.data
        config_details.branding_email = form.branding_email.data
        config_details.posts_per_page = form.posts_per_page.data
        config_details.allowed_extensions = form.allowed_extensions.data
        config_details.ticket_upload_folder = form.ticket_upload_folder.data
        config_details.base_url = form.base_url.data

        config_details.use_auth_domain = form.use_auth_domain.data
        config_details.auth_domain = form.auth_domain.data or False

        config_details.csv_dump_limit = form.csv_dump_limit.data

        config_details.change_category = form.change_category.data or False
        config_details.change_category_only_admin_or_super_user = form.change_category_only_admin_or_super_user.data

        # Don't change the password if nothing was entered.
        if form.mail_password.data != '':
            config_details.mail_password = form.mail_password.data
        # save the branding logo if a new one was selected.
        logo_file = request.files.get('branding_logo')
        if logo_file is not None and logo_file.filename != '':
            uploaded_logo = UploadFile(logo_file)
            uploaded_logo.upload_folder = app.config['avatar_upload_folder']
            if uploaded_logo.upload_file():
                # delete the old logo if it exists and is different.
                if (config_details.branding_logo
                        and config_details.branding_logo != uploaded_logo.file_name):
                    old_logo = os.path.join(app.config['avatar_upload_folder'], config_details.branding_logo)
                    if os.path.exists(old_logo):
                        os.remove(old_logo)
                config_details.branding_logo = uploaded_logo.file_name
            else:
                flash(gettext('There was a problem uploading the logo file.'), category='warning')

        db.session.commit()
        flash(gettext('Config details updated.'), category='success')
        return redirect(url_for('admin_bp.config'))

    # populate form with details from database.
    form.mail_server.data = config_details.mail_server
    form.mail_port.data = config_details.mail_port
    form.mail_use_tls.data = config_details.mail_use_tls
    form.mail_use_ssl.data = config_details.mail_use_ssl
    form.mail_debug.data = config_details.mail_debug
    form.mail_username.data = config_details.mail_username
    form.mail_password.data = config_details.mail_password
    form.mail_default_sender.data = config_details.mail_default_sender
    form.mail_max_emails.data = config_details.mail_max_emails
    form.mail_suppress_send.data = config_details.mail_suppress_send
    form.mail_ascii_attachments.data = config_details.mail_ascii_attachments

    form.application_title.data = config_details.application_title
    form.branding_company_name.data = config_details.branding_company_name
    form.branding_phone.data = config_details.branding_phone
    form.branding_email.data = config_details.branding_email

    form.posts_per_page.data = config_details.posts_per_page
    form.allowed_extensions.data = config_details.allowed_extensions
    form.ticket_upload_folder.data = config_details.ticket_upload_folder
    form.base_url.data = config_details.base_url

    form.use_auth_domain.data = config_details.use_auth_domain
    form.auth_domain.data = config_details.auth_domain

    form.csv_dump_limit.data = config_details.csv_dump_limit

    form.change_category.data = config_details.change_category
    form.change_category_only_admin_or_super_user.data = config_details.change_category_only_admin_or_super_user

    return render_template('admin_config.html',
                           title=gettext('Flicket Configuration'),
                           form=form,
                           config_details=config_details)
