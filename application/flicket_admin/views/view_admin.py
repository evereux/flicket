#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

import datetime

from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_babel import gettext
from flask_login import current_user
from flask_login import login_required
from flask_principal import identity_loaded
from flask_principal import Permission
from flask_principal import Principal
from flask_principal import RoleNeed
from flask_principal import UserNeed

from application import app, db
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.models.flicket_user import FlicketGroup
from application.flicket.scripts.hash_password import hash_password
from application.flicket_admin.forms.forms_admin import AddGroupForm
from application.flicket_admin.forms.forms_admin import AddUserForm
from application.flicket_admin.forms.forms_admin import EnterPasswordForm
from application.flicket_admin.forms.forms_admin import EditUserForm
from . import admin_bp

principals = Principal(app)
# define flicket_admin role need
admin_only = RoleNeed('flicket_admin')
admin_permission = Permission(admin_only)


def create_user(username, password, email=None, name=None, job_title=None, locale=None, disabled=None):
    password = hash_password(password)
    register = FlicketUser(username=username,
                           email=email,
                           name=name,
                           password=password,
                           job_title=job_title,
                           date_added=datetime.datetime.now(),
                           locale=locale,
                           disabled=disabled)
    db.session.add(register)
    db.session.commit()


# add permissions
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # set the identity user object
    identity.user = current_user
    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of groups, update the
    # identity with the groups that the user provides
    if hasattr(current_user, 'flicket_groups'):
        the_user = FlicketUser.query.filter_by(id=current_user.id).first()
        for g in the_user.flicket_groups:
            identity.provides.add(RoleNeed('{}'.format(g.group_name)))


@admin_bp.route(app.config['ADMINHOME'])
@login_required
@admin_permission.require(http_exception=403)
def index():
    # noinspection PyUnresolvedReferences
    return render_template('admin.html', title='Admin')


# shows all users
@admin_bp.route(app.config['ADMINHOME'] + 'users/', methods=['GET', 'POST'])
@admin_bp.route(app.config['ADMINHOME'] + 'users/<int:page>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def users(page=1):
    users = FlicketUser.query.order_by(FlicketUser.username)
    users = users.paginate(page=page, per_page=app.config['posts_per_page'])

    # noinspection PyUnresolvedReferences
    return render_template('admin_users.html', title='Users', users=users)


# add user
@admin_bp.route(app.config['ADMINHOME'] + 'add_user/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        create_user(form.username.data,
                    form.password.data,
                    email=form.email.data,
                    name=form.name.data,
                    job_title=form.job_title.data,
                    locale=form.locale.data,
                    disabled=form.disabled.data)
        flash(gettext('You have successfully registered new user "{}".'.format(form.username.data)), category='success')
        return redirect(url_for('admin_bp.users'))
    # noinspection PyUnresolvedReferences
    return render_template('admin_user.html', title='Add User', form=form)


# edit user
@admin_bp.route(app.config['ADMINHOME'] + 'edit_user/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def edit_user():
    _id = request.args.get('id')
    user = FlicketUser.query.filter_by(id=_id).first()
    if user:
        form = EditUserForm()
        if form.validate_on_submit():
            # check the username is unique
            if user.username != form.username.data:
                query = FlicketUser.query.filter_by(username=form.username.data)
                if query.count() > 0:
                    flash(gettext('Username already exists'), category='warning')
                else:
                    # change the username.
                    user.username = form.username.data
            # Don't change the password if nothing was entered.
            if form.password.data != '':
                user.password = hash_password(form.password.data)

            user.email = form.email.data
            user.name = form.name.data
            user.job_title = form.job_title.data
            user.disabled = form.disabled.data

            groups = form.groups.data
            # bit hacky but until i get better at this.
            # at least it keeps the groups table clean. :/
            # delete all groups associated with current user.
            user.flicket_groups = []  # this is beautifully simple though
            # add the user to selected groups
            for g in groups:
                group_id = FlicketGroup.query.filter_by(id=g).first()
                group_id.users.append(user)
            db.session.commit()
            flash(gettext("User {} edited.".format(user.username)), category='success')
            return redirect(url_for('admin_bp.edit_user', id=_id))

        # populate form with form data retrieved from database.
        form.user_id.data = user.id
        form.username.data = user.username
        form.email.data = user.email
        form.name.data = user.name
        form.job_title.data = user.job_title
        form.disabled.data = user.disabled
        # define list of preselect groups.
        groups = []
        for g in user.flicket_groups:
            groups.append(g.id)
        form.groups.data = groups
    else:
        flash(gettext("Could not find user."), category='warning')
        return redirect(url_for('admin_bp.index'))

    # noinspection PyUnresolvedReferences
    return render_template('admin_user.html',
                           title='Edit User',
                           admin_edit=True,
                           form=form, user=user)


# Delete user
@admin_bp.route(app.config['ADMINHOME'] + 'delete_user/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def delete_user():
    form = EnterPasswordForm()
    id = request.args.get('id')
    user_details = FlicketUser.query.filter_by(id=id).first()

    # we won't ever delete the flicket_admin user (id = 1)
    if id == '1':
        flash(gettext('Can\'t delete default flicket_admin user.'), category='warning')
        return redirect(url_for('admin_bp.index'))

    if form.validate_on_submit():
        # delete the user.
        flash(gettext('Deleted user {}s'.format(user_details.username)), category='success')
        db.session.delete(user_details)
        db.session.commit()
        return redirect(url_for('admin_bp.users'))
    # populate form with logged in user details
    form.id.data = g.user.id
    # noinspection PyUnresolvedReferences
    return render_template('admin_delete_user.html', title='Delete user',
                           user_details=user_details, form=form)


# Add new groups
@admin_bp.route(app.config['ADMINHOME'] + 'groups/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def groups():
    form = AddGroupForm()
    groups = FlicketGroup.query.all()
    if form.validate_on_submit():
        add_group = FlicketGroup(
            group_name=form.group_name.data
        )
        db.session.add(add_group)
        db.session.commit()
        flash(gettext('New group "{}" added.'.format(form.group_name.data)), category='success')
        return redirect(url_for('admin_bp.groups'))

    # noinspection PyUnresolvedReferences
    return render_template('admin_groups.html', title='Groups', form=form, groups=groups)


# Edit groups
@admin_bp.route(app.config['ADMINHOME'] + 'edit_group/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_edit_group():
    form = AddGroupForm()
    id = request.args.get('id')
    group = FlicketGroup.query.filter_by(id=id).first()

    # if group can't be found in database.
    if not group:
        flash(gettext('Could not find group {}'.format(group.group_name)), category='warning')
        return redirect(url_for('admin_bp.index'))

    # prevent editing of flicket_admin group name as this is hard coded into flicket_admin view permissions.
    if group.group_name == app.config['ADMIN_GROUP_NAME']:
        flash(gettext('Can\'t edit group {}s.'.format(app.config["ADMIN_GROUP_NAME"])), category='warning')
        return redirect(url_for('admin_bp.index'))

    if form.validate_on_submit():
        group.group_name = form.group_name.data
        db.session.commit()
        flash(gettext('Group name changed to {}.'.format(group.group_name)), category='success')
        return redirect(url_for('admin_bp.groups'))
    form.group_name.data = group.group_name

    # noinspection PyUnresolvedReferences
    return render_template('admin_edit_group.html', title='Edit Group', form=form)


# Delete group
@admin_bp.route(app.config['ADMINHOME'] + 'delete_group/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_delete_group():
    form = EnterPasswordForm()
    id = request.args.get('id')
    group_details = FlicketGroup.query.filter_by(id=id).first()

    # we won't ever delete the flicket_admin group (id = 1)
    if id == '1':
        flash(gettext('Can\'t delete default flicket_admin group.'), category='warning')
        return redirect(url_for('admin_bp.index'))

    if form.validate_on_submit():
        # delete the group.
        flash(gettext('Deleted group {}s'.format(group_details.group_name)), category="info")
        db.session.delete(group_details)
        db.session.commit()
        return redirect(url_for('admin_bp.groups'))
    # populate form with logged in user details
    form.id.data = g.user.id
    title = gettext('Delete Group')
    # noinspection PyUnresolvedReferences
    return render_template('admin_delete_group.html', title=title,
                           group_details=group_details, form=form)
