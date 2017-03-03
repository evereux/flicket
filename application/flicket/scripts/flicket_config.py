#! usr/bin/python3
# -*- coding: utf8 -*-

from application import app
from application.flicket_admin.models.flicket_config import FlicketConfig

def set_flicket_config():
    """
    Updates the flicket application settings based on the values stored in the database.
    :return:
    """
    config = FlicketConfig.query.first()

    app.config.update(
        posts_per_page=config.posts_per_page,
        allowed_extensions=config.allowed_extensions.split(', '),
        ticket_upload_folder=config.ticket_upload_folder,
    )
