#! usr/bin/python3
# -*- coding: utf8 -*-

import datetime

from flask import flash, redirect, render_template, url_for

from application import app, db
from application.flicket.forms.forms_main import RegisterForm
from application.flicket.models.user import User
from application.flicket.scripts.hash_password import hash_password
from . import flicket_bp


# Register page
@flicket_bp.route(app.config['WEBHOME'] + 'register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = hash_password(form.password.data)
        _register = User(username=form.username.data,
                         email=form.email.data,
                         name=form.name.data,
                         password=password,
                         date_added=datetime.datetime.now())
        db.session.add(_register)
        db.session.commit()
        flash('You have successfully registered.')
        return redirect(url_for('flicket_bp.login'))
    return render_template('register.html', title='Register', form=form)
