#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from application import db
from application.flicket.models import Base


class FlicketConfig(Base):
    """
    Server configuration table editable by administrators only.

    For email configuration settings see https://flask-mail.readthedocs.io/en/latest/ for more information.

    posts_per_page: dictates how many posts are displayed per page for flicket application.
    allowed_extensions: a comma delimited list of file extensions users are allowed to attach to a post.
    ticket_upload_folder: folder into which uploads are stored.
    base_url: site base url eg http://yourwebsite.com:8000
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
    mail_use_tls = db.Column(db.BOOLEAN)
    mail_use_ssl = db.Column(db.BOOLEAN)
    mail_debug = db.Column(db.BOOLEAN)
    mail_username = db.Column(db.String(128))
    mail_password = db.Column(db.String(256))
    mail_default_sender = db.Column(db.String(128))
    mail_max_emails = db.Column(db.Integer)
    mail_suppress_send = db.Column(db.BOOLEAN)
    mail_ascii_attachments = db.Column(db.BOOLEAN)

    posts_per_page = db.Column(db.Integer)
    allowed_extensions = db.Column(db.String(256))
    ticket_upload_folder = db.Column(db.String(256))
    avatar_upload_folder = db.Column(db.String(256))

    application_title = db.Column(db.String(32))

    base_url = db.Column(db.String(128))

    auth_domain = db.Column(db.String(64))
    use_auth_domain = db.Column(db.BOOLEAN, default=False)
