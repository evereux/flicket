#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, redirect, url_for, render_template, g
from flask_login import login_required

from application import app, db
from application.flicket.forms.forms_main import EditUserForm
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.functions_login import check_password_format
from application.flicket.scripts.hash_password import hash_password
from . import flicket_bp


# edit self page
@flicket_bp.route(app.config['WEBHOME'] + 'user_details', methods=['GET', 'POST'])
@login_required
def user_details():
    form = EditUserForm()

    if form.validate_on_submit():

        # find the user in db to edit
        user = FlicketUser.query.filter_by(id=g.user.id).first()
        user.name = form.name.data
        user.email = form.email.data
        flash('You have edited your user details.', category='success')

        password = form.new_password.data
        if (password != '') and (check_password_format(password)):
            password = hash_password(password)
            user.password = password
            flash('You have changed your password.', category='success')

        db.session.commit()

        return redirect(url_for('flicket_bp.user_details'))

    form.name.data = g.user.name
    form.email.data = g.user.email
    form.username.data = g.user.username

    return render_template('flicket_edituser.html', form=form, title='Edit User Details')
