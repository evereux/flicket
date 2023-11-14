#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import url_for

from application import app


class PaginatedAPIMixin(object):

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total,
            },
            '_links': {
                'self': app.config['base_url'] + url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': app.config['base_url'] + url_for(endpoint, page=page + 1, per_page=per_page,
                                                         **kwargs) if resources.has_next else None,
                'prev': app.config['base_url'] + url_for(endpoint, page=page - 1, per_page=per_page,
                                                         **kwargs) if resources.has_prev else None,
            },
        }

        return data
