#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from application import db
from application.flicket.models import Base


class FlicketConfig(Base):
    """
    Server configuration settings editable by administrators only via the administration page `/flicket_admin/config/`.

    For email configuration settings see https://flask-mail.readthedocs.io/en/latest/ for more information.

    :param str mail_server: example: `smtp.yourcompany.com`.
    :param int mail_port: example: `567`
    :param bool mail_use_tls: example: `true`
    :param bool mail_use_ssl: example: `false`
    :param bool mail_debug: example: `false`
    :param str mail_username: example: `flicket.admin`
    :param str mail_password:
    :param str mail_default_sender: example: `flicket.admin@yourcompany.com`
    :param int mail_max_emails:
    :param bool mail_suppress_send:
    :param bool mail_ascii_attachments:
    :param str application_title: Changes the default banner text from `Flicket`. Can typically be your company name.
    :param str posts_per_page: Maximum number of posts / topics displayed per page.
    :param str allowed_extensions: A comma delimited list of file extensions users are allowed to upload. DO NOT include
      the . before the extension letter.
    :param str ticket_upload_folder: The folder used for file uploads.
    :param str base_url: The sites base url. This is used to resolve urls for emails and links. Broken links are
      probably a result of not setting this value.
    :param str csv_dump_limit: The maximum number of rows exported to csv.
    :param bool change_category: Enable/disable change category.
    :param bool change_category_only_admin_or_super_user: Only admins or super users can change category.

    """
    __tablename__ = 'flicket_config'

    def __init__(self, **kwargs):
        """
        Initialisation used for initial setup.py file.
        :param kwargs:
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    id = db.Column(db.Integer, primary_key=True)

    # mail settings for Flask-Mail
    mail_server = db.Column(db.String(128))
    mail_port = db.Column(db.Integer)
    mail_use_tls = db.Column(db.BOOLEAN, default=False)
    mail_use_ssl = db.Column(db.BOOLEAN, default=False)
    mail_debug = db.Column(db.BOOLEAN, default=False)
    mail_username = db.Column(db.String(128))
    mail_password = db.Column(db.String(256))
    mail_default_sender = db.Column(db.String(128))
    mail_max_emails = db.Column(db.Integer)
    mail_suppress_send = db.Column(db.BOOLEAN, default=False)
    mail_ascii_attachments = db.Column(db.BOOLEAN, default=False)

    posts_per_page = db.Column(db.Integer)
    allowed_extensions = db.Column(db.String(256))
    ticket_upload_folder = db.Column(db.String(256))
    avatar_upload_folder = db.Column(db.String(256))

    application_title = db.Column(db.String(32))

    base_url = db.Column(db.String(128))

    auth_domain = db.Column(db.String(64))
    use_auth_domain = db.Column(db.BOOLEAN, default=False)

    csv_dump_limit = db.Column(db.Integer, default=1000)

    # features
    change_category = db.Column(db.BOOLEAN, default=False)
    change_category_only_admin_or_super_user = db.Column(db.BOOLEAN, default=False)

    @staticmethod
    def extension_allowed(filename):
        """
        Validates extension of a given filename and returns True if valid. Otherwise False.
        :param filename:
        :return:
        """

        extension = filename.rsplit('.', 1)[1]

        if extension.lower() in FlicketConfig.valid_extensions():
            return True

        return False

    @staticmethod
    def valid_extensions():
        """
        Returns a list of valid extensions.
        :return: list()
        """

        config = FlicketConfig.query.one()

        extensions = config.allowed_extensions.split(',')
        extensions = [i.strip() for i in extensions]

        return extensions

    def __repr__(self):
        return "<FlicketConfig model class>"
