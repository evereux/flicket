#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

from application.flicket.scripts.functions_login import check_email_format

form_class_button = {'class': 'btn btn-primary btn-sm'}


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
    mail_server = StringField(lazy_gettext('mail_server'), validators=[])
    mail_port = IntegerField(lazy_gettext('mail_port'), validators=[NumberRange(min=1, max=65535)])
    mail_use_tls = BooleanField(lazy_gettext('mail_use_tls'), validators=[])
    mail_use_ssl = BooleanField(lazy_gettext('mail_use_ssl'), validators=[])
    mail_debug = BooleanField(lazy_gettext('mail_debug'), validators=[])
    mail_username = StringField(lazy_gettext('mail_username'), validators=[])
    mail_password = PasswordField(lazy_gettext('mail_password'), validators=[])
    mail_default_sender = StringField(lazy_gettext('mail_default_sender'), validators=[])
    mail_max_emails = IntegerField(lazy_gettext('mail_max_emails'), validators=[])
    mail_suppress_send = BooleanField(lazy_gettext('mail_suppress_send'), validators=[])
    mail_ascii_attachments = BooleanField(lazy_gettext('mail_ascii_attachments'), validators=[])

    application_title = StringField(lazy_gettext('application_title'),
                                    validators=[DataRequired(), Length(min=3, max=32)])
    posts_per_page = IntegerField(lazy_gettext('posts_per_page'),
                                  validators=[DataRequired(), NumberRange(min=10, max=200)])
    allowed_extensions = StringField(lazy_gettext('allowed_extensions'), validators=[DataRequired()])
    ticket_upload_folder = StringField(lazy_gettext('ticket_upload_folder'), validators=[DataRequired()])
    base_url = StringField(lazy_gettext('base_url'), validators=[Length(min=0, max=128)])

    use_auth_domain = BooleanField(lazy_gettext('use_auth_domain'), validators=[])
    auth_domain = StringField(lazy_gettext('auth_domain'), validators=[])

    csv_dump_limit = IntegerField(lazy_gettext('csv_dump_limit'), validators=[])

    change_category = BooleanField(lazy_gettext('change_category'), validators=[])
    change_category_only_admin_or_super_user = BooleanField(lazy_gettext('change_category_only_admin_or_super_user'),
                                                            validators=[])

    submit = SubmitField(lazy_gettext('Submit'), render_kw=form_class_button, validators=[DataRequired()])


class EmailTest(FlaskForm):
    email_address = StringField(lazy_gettext('email_address'), validators=[DataRequired(), check_email_formatting])

    submit = SubmitField(lazy_gettext('Submit'), render_kw=form_class_button, validators=[DataRequired()])
