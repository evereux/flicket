#! python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""
    Queues
    ======

    Get Queue By Category ID
    ~~~~~~~~~~~~~~~~~~~~~~~~

    .. http:get:: /flicket-api/queue/(int:category_id)

    Get Queues
    ~~~~~~~~~~

    .. http:get:: /flicket-api/queues/
"""

from flask import jsonify, request, url_for

from .sphinx_helper import api_url
from . import bp_api
from application import app, db
from application.flicket.models.flicket_models import FlicketQueue
from application.flicket_api.views.auth import token_auth
from application.flicket_api.views.errors import bad_request


@bp_api.route(api_url + 'queue/<int:id>', methods=['GET'])
@token_auth.login_required
def get_queue(id):
    return jsonify(FlicketQueue.query.get_or_404(id).to_dict())


@bp_api.route(api_url + 'queues/', methods=['GET'])
@token_auth.login_required
def get_queues():
    name = request.args.get('name')
    department_id = request.args.get('department_id')
    department = request.args.get('department')
    queues = FlicketQueue.query.order_by(FlicketQueue.queue)
    kwargs = {}
    if name:
        queues = queues.filter(FlicketQueue.queue.ilike(f'%{name}%'))
        kwargs['name'] = name
    if department_id:
        queues = queues.filter(department_id=department_id)
        kwargs['department_id'] = department_id
    if department:
        queues = queues.filter(FlicketQueue.department.ilike(f'%{department}'))
        kwargs['department'] = department
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', app.config['posts_per_page'], type=int), 100)
    data = FlicketQueue.to_collection_dict(queues, page, per_page, 'bp_api.get_queues', **kwargs)
    return jsonify(data)
