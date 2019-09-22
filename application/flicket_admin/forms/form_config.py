#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

from application.flicket.scripts.functions_login import check_email_format

form_class_button = {'class': 'btn btn-primary'}


def check_email_formatting(form, field):
    """
    Checks formatting of email and also checks that a user is not already registered with the same email address
    :param form:
    :param field:
    :return:
    """
    ok = True
    if not check_email_format(form.email_address.data):
        field.errors.append('Please enter a correctly formatted email address.')
        ok = False

    return ok


class ConfigForm(FlaskForm):
    mail_server = StringField('mail_server', validators=[])
    mail_port = IntegerField('mail_port', validators=[NumberRange(min=1, max=65535)])
    mail_use_tls = BooleanField('mail_use_tls', validators=[])
    mail_use_ssl = BooleanField('mail_use_ssl', validators=[])
    mail_debug = BooleanField('mail_debug', validators=[])
    mail_username = StringField('mail_username', validators=[])
    mail_password = PasswordField('mail_password', validators=[])
    mail_default_sender = StringField('mail_default_sender', validators=[])
    mail_max_emails = IntegerField('mail_max_emails', validators=[])
    mail_suppress_send = BooleanField('mail_suppress_send', validators=[])
    mail_ascii_attachments = BooleanField('mail_ascii_attachments', validators=[])

    application_title = StringField('application_title', validators=[DataRequired(), Length(min=3, max=32)])
    posts_per_page = IntegerField('posts_per_page', validators=[DataRequired(), NumberRange(min=10, max=200)])
    allowed_extensions = StringField('allowed_extensions', validators=[DataRequired()])
    ticket_upload_folder = StringField('ticket_upload_folder', validators=[DataRequired()])
    base_url = StringField('base_url', validators=[Length(min=0, max=128)])

    use_auth_domain = BooleanField('use_auth_domain', validators=[])
    auth_domain = StringField('auth_domain', validators=[])

    csv_dump_limit = IntegerField('csv_dump_limit', validators=[])

    submit = SubmitField('Submit', render_kw=form_class_button, validators=[DataRequired()])


class EmailTest(FlaskForm):
    email_address = StringField('email_address', validators=[DataRequired(), check_email_formatting])

    submit = SubmitField('Submit', render_kw=form_class_button, validators=[DataRequired()])
