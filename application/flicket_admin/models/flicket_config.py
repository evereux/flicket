#! usr/bin/python3
# -*- coding: utf8 -*-

from application import db
from application.flicket.models import Base

class FlicketConfig(Base):
    """
    Server email configuration settings. https://flask-mail.readthedocs.io/en/latest/ for
    more information.
    """
    __tablename__ = 'flicket_config'

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)


    id = db.Column(db.Integer, primary_key=True)
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


