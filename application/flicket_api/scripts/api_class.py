#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import json

from application.flicket_api.views.api import api_departments, api_categories, api_statuses


class FlicketApi(object):
    """
    Class to access Flicket api views and return json decoded data.
    """

    @staticmethod
    def get_departments():

        return json.loads(api_departments())

    @staticmethod
    def get_categories():

        return json.loads(api_categories())

    @staticmethod
    def get_statuses():

        return json.loads(api_statuses())

