import datetime

import bcrypt
from flask import (flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   url_for)
from flask_login import login_required, current_user
from flask_principal import Permission, Principal, RoleNeed

from application import app, db
from application.admin.models.user import User, Group
from application.flicket.forms.forms_main import RegisterForm
from application.flicket.scripts.hash_password import hash_password
from application.home.forms.forms_admin import AddGroupForm, EditUserForm, EnterPasswordForm
# ! usr/bin/python3
# -*- coding: utf8 -*-

from . import admin_bp

principals = Principal(app)
# define admin role need
admin_only = RoleNeed('admin')
admin_permission = Permission(admin_only)


@admin_bp.route(app.config['ADMINHOME'])
@login_required
@admin_permission.require(http_exception=403)
def index():
    return render_template('admin.html', title='Admin')


@admin_bp.route(app.config['ADMINHOME'] + 'add_user/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def add_user():
    form = RegisterForm()
    if form.validate_on_submit():
        password = hash_password(form.password.data)
        register = User(username=form.username.data,
                        email=form.email.data,
                        name=form.name.data,
                        password=password,
                        date_added=datetime.datetime.now())
        db.session.add(register)
        db.session.commit()
        flash('You have succesfully registered new user {}.'.format(form.username.data))
        return redirect(url_for('admin_bp.admin_users'))
    return render_template('admin_add_user.html', title='Add User', form=form)


# edit users: display list of users, select which to edit
@admin_bp.route(app.config['ADMINHOME'] + 'admin_users/', methods=['GET', 'POST'])
@admin_bp.route(app.config['ADMINHOME'] + 'admin_users/<int:page>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_users(page=1):
    users = User.query.order_by(User.username)
    users = users.paginate(page, app.config['POSTS_PER_PAGE'])

    return render_template('admin_users.html', title='Users', users=users)


# edit user
@admin_bp.route(app.config['ADMINHOME'] + 'admin_edit_user/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_edit_user():
    form = EditUserForm()
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()
    if user:
        if form.validate_on_submit():
            # check the username is unique
            if (user.username != form.username.data):
                query = User.query.filter_by(username=form.username.data)
                if query.count() > 0:
                    flash('Username already exists')
                else:
                    # change the username.
                    user.username = form.username.data
            user.email = form.email.data
            user.name = form.name.data
            groups = form.groups.data
            # bit hacky but until i get better at this.
            # at least it keeps the groups table clean. :/
            # delete all groups associated with current user.
            user.groups = []  # this is beautifully simply though
            # add the user to selected groups
            for g in groups:
                group_id = Group.query.filter_by(id=g).first()
                group_id.users.append(user)
            db.session.commit()
            flash("User {} edited.".format(user.username))
            return redirect(url_for('admin_bp.admin_users'))

        # populate form with form data retrieved from database.
        form.username.data = user.username
        form.email.data = user.email
        form.name.data = user.name
        # define list of preselect groups.
        groups = []
        for g in user.groups:
            groups.append(g.id)
        form.groups.data = groups
    else:
        flash("Could not find user.")
        return redirect(url_for('admin'))

    return render_template('admin_edit_user.html', title='Edit User', form=form, user=user)


# Delete user
@admin_bp.route(app.config['ADMINHOME'] + 'admin_delete_user/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_delete_user():
    form = EnterPasswordForm()
    id = request.args.get('id')
    user_details = User.query.filter_by(id=id).first()

    # we won't ever delete the admin user (id = 1)
    if id == '1':
        flash('Can\'t delete default admin user.')
        return redirect(url_for('admin_bp.admin'))

    if form.validate_on_submit():
        # delete the user.
        flash('Deleted user {}'.format(user_details.username))
        db.session.delete(user_details)
        db.session.commit()
        return redirect(url_for('admin_users'))
    # populate form with logged in user details
    form.id.data = g.user.id
    return render_template('admin_delete_user.html', title='Delete user',
                           user_details=user_details, form=form)


# Add new groups
@admin_bp.route(app.config['ADMINHOME'] + 'admin_groups/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_groups():
    form = AddGroupForm()
    groups = Group.query.all()
    if form.validate_on_submit():
        add_group = Group(
            group_name=form.group_name.data
        )
        db.session.add(add_group)
        db.session.commit()
        flash('New group "{}" added.'.format(form.group_name.data))
        return redirect(url_for('admin_bp.admin_groups'))

    return render_template('admin_groups.html', title='Groups', form=form, groups=groups)


# Edit groups
@admin_bp.route(app.config['ADMINHOME'] + 'admin_edit_group/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_edit_group():
    form = AddGroupForm()
    id = request.args.get('id')
    group = Group.query.filter_by(id=id).first()

    # if group can't be found in database.
    if not group:
        flash('Could not find group {}'.format(group.group_name))
        return redirect(url_for('admin_bp.index'))

    # prevent editing of admin group name as this is hard coded into admin view permissions.
    if group.group_name == app.config['ADMIN_GROUP_NAME']:
        flash('Can\'t edit group {}'.format(app.config['ADMIN_GROUP_NAME']))
        return redirect(url_for('admin'))

    if form.validate_on_submit():
        group.group_name = form.group_name.data
        db.session.commit()
        return redirect(url_for('admin_bp.admin_groups'))
    form.group_name.data = group.group_name

    return render_template('admin_edit_group.html', title='Edit Group', form=form)


# Delete group
@admin_bp.route(app.config['ADMINHOME'] + 'admin_delete_group/', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_delete_group():
    form = EnterPasswordForm()
    id = request.args.get('id')
    group_details = Group.query.filter_by(id=id).first()

    # we won't ever delete the admin group (id = 1)
    if id == '1':
        flash('Can\'t delete default admin group.')
        return redirect(url_for('admin'))

    if form.validate_on_submit():
        # delete the group.
        flash('Deleted group {}'.format(group_details.group_name))
        db.session.delete(group_details)
        db.session.commit()
        return redirect(url_for('admin_bp.admin_groups'))
    # populate form with logged in user details
    form.id.data = g.user.id
    return render_template('admin_delete_group.html', title='Delete Group',
                           group_details=group_details, form=form)
