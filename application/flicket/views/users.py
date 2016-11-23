#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from application import app
from application.admin.models.user import User
from application.flicket.forms.flicket_forms import SearchUserForm
from application.flicket.scripts.flicket_user_details import FlicketUserDetails
from . import flicket_bp


# view users
@flicket_bp.route(app.config['FLICKETHOME'] + 'users/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKETHOME'] + 'users/<int:page>/', methods=['GET', 'POST'])
@login_required
def flicket_users(page=1):
    form = SearchUserForm()

    filter = request.args.get('filter')

    if form.validate_on_submit():
        return redirect(url_for('flicket_bp.flicket_users', filter=form.name.data))

    users = User.query

    if filter:
        filter_1 = User.username.ilike('%{}%'.format(filter))
        filter_2 = User.name.ilike('%{}%'.format(filter))
        users = users.filter(filter_1 | filter_2)
        form.name.data = filter

    users = users.order_by(User.username.asc())
    users = users.paginate(page, app.config['POSTS_PER_PAGE'])

    return render_template('flicket_users.html',
                           title='Flicket - Users',
                           users=users,
                           form=form,
                           details=FlicketUserDetails)
