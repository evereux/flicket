#! usr/bin/python3
# -*- coding: utf-8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import flash, g, redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.flicket.forms.forms_main import EditUserForm
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_upload import UploadAvatar
from application.flicket.scripts.functions_login import check_password_format, password_requirements
from application.flicket.scripts.hash_password import hash_password
from . import flicket_bp


# edit self page
@flicket_bp.route(app.config['WEBHOME'] + 'user_details', methods=['GET', 'POST'])
@login_required
def user_details():
    form = EditUserForm()

    if form.validate_on_submit():

        if 'avatar' in request.files:
            avatar = request.files['avatar']
            filename = avatar.filename
        else:
            avatar = False
            filename = ''

        if filename != '':
            # upload the avatar
            upload_avatar = UploadAvatar(avatar, g.user)
            if upload_avatar.upload_file() is False:
                flash('There was a problem uploading files. Please ensure you are using a valid image file name.',
                      category='danger')
                return redirect(url_for('flicket_bp.user_details'))
            avatar_filename = upload_avatar.file_name
        else:
            avatar_filename = None

        # find the user in db to edit
        user = FlicketUser.query.filter_by(id=g.user.id).first()

        # update details, if changed
        if user.name != form.name.data:
            user.name = form.name.data
            flash('You have changed your "name".', category='success')
        if user.email != form.email.data:
            user.email = form.email.data
            flash('You have changed your "email".', category='success')
        if user.job_title != form.job_title.data:
            user.job_title = form.job_title.data
            flash('You have changed your "job title".', category='success')
        if user.locale != form.locale.data:
            user.locale = form.locale.data
            flash('You have changed your "locale".', category='success')

        if avatar_filename:
            user.avatar = avatar_filename

        # change the password if the user has entered a new password.
        password = form.new_password.data
        if (password != '') and (check_password_format(password, user.username, user.email)):
            password = hash_password(password)
            user.password = password
            flash('You have changed your password.', category='success')
        elif password != '':
            flash('Password not changed.', category='warning')
            flash(password_requirements, category='warning')

        db.session.commit()

        return redirect(url_for('flicket_bp.user_details'))

    form.name.data = g.user.name
    form.email.data = g.user.email
    form.username.data = g.user.username
    form.job_title.data = g.user.job_title
    form.locale.data = g.user.locale

    return render_template('flicket_edituser.html', form=form, title='Edit User Details')
