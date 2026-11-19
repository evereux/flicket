#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, PasswordField, FileField
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


def check_branding_email(form, field):
    """
    Checks that the branding email is correctly formatted.
    :param form:
    :param field:
    :return:
    """
    if field.data and not check_email_format(field.data):
        field.errors.append('Please enter a correctly formatted email address.')


class ConfigForm(FlaskForm):
    mail_server = StringField(lazy_gettext('Mail server'), validators=[])
    mail_port = IntegerField(lazy_gettext('Mail port'), validators=[NumberRange(min=1, max=65535)])
    mail_use_tls = BooleanField(lazy_gettext('Use TLS'), validators=[])
    mail_use_ssl = BooleanField(lazy_gettext('Use SSL'), validators=[])
    mail_debug = BooleanField(lazy_gettext('Mail debug'), validators=[])
    mail_username = StringField(lazy_gettext('Mail username'), validators=[])
    mail_password = PasswordField(lazy_gettext('Mail password'), validators=[])
    mail_default_sender = StringField(lazy_gettext('Default sender'), validators=[])
    mail_max_emails = IntegerField(lazy_gettext('Max emails'), validators=[])
    mail_suppress_send = BooleanField(lazy_gettext('Suppress sending'), validators=[])
    mail_ascii_attachments = BooleanField(lazy_gettext('ASCII attachments'), validators=[])

    application_title = StringField(lazy_gettext('Application title'),
                                    validators=[DataRequired(), Length(min=3, max=32)])

    branding_company_name = StringField(lazy_gettext('Company name'),
                                         validators=[DataRequired(), Length(min=1, max=64)])
    branding_phone = StringField(lazy_gettext('Phone'), validators=[Length(min=0, max=32)])
    branding_email = StringField(lazy_gettext('Email'),
                                 validators=[Length(max=128), check_branding_email])
    branding_logo = FileField(lazy_gettext('Logo'), validators=[])
    posts_per_page = IntegerField(lazy_gettext('Posts per page'),
                                  validators=[DataRequired(), NumberRange(min=10, max=200)])
    allowed_extensions = StringField(lazy_gettext('Allowed extensions'), validators=[DataRequired()])
    ticket_upload_folder = StringField(lazy_gettext('Ticket upload folder'), validators=[DataRequired()])
    base_url = StringField(lazy_gettext('Base URL'), validators=[Length(min=0, max=128)])

    use_auth_domain = BooleanField(lazy_gettext('Use auth domain'), validators=[])
    auth_domain = StringField(lazy_gettext('Auth domain'), validators=[])

    csv_dump_limit = IntegerField(lazy_gettext('CSV dump limit'), validators=[])

    change_category = BooleanField(lazy_gettext('Allow changing category'), validators=[])
    change_category_only_admin_or_super_user = BooleanField(lazy_gettext('Only admins and super users can change category'),
                                                            validators=[])

    submit = SubmitField(lazy_gettext('Submit'), render_kw=form_class_button, validators=[DataRequired()])


class EmailTest(FlaskForm):
    email_address = StringField(lazy_gettext('Email address'), validators=[DataRequired(), check_email_formatting])

    submit = SubmitField(lazy_gettext('Submit'), render_kw=form_class_button, validators=[DataRequired()])
