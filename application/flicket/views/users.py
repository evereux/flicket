#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from application import app
from application.flicket.forms.flicket_forms import SearchUserForm
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_user_details import FlicketUserDetails
from . import flicket_bp


# view users
@flicket_bp.route(app.config['FLICKET'] + 'users/', methods=['GET', 'POST'])
@flicket_bp.route(app.config['FLICKET'] + 'users/<int:page>/', methods=['GET', 'POST'])
@login_required
def flicket_users(page=1):
    form = SearchUserForm()

    filter = request.args.get('filter')

    if form.validate_on_submit():
        return redirect(url_for('flicket_bp.flicket_users', filter=form.name.data))

    users = FlicketUser.query

    if filter:
        filter_1 = FlicketUser.username.ilike('%{}%'.format(filter))
        filter_2 = FlicketUser.name.ilike('%{}%'.format(filter))
        users = users.filter(filter_1 | filter_2)
        form.name.data = filter

    users = users.order_by(FlicketUser.username.asc())
    users = users.paginate(page, app.config['posts_per_page'])

    return render_template('flicket_users.html',
                           title='Flicket - Users',
                           users=users,
                           form=form,
                           details=FlicketUserDetails)
