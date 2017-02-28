#! usr/bin/python3
# -*- coding: utf8 -*-

from urllib.parse import urlparse, urljoin

from flask import (flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
from flask_login import (current_user,
                         login_user,
                         logout_user)
from flask_mail import Mail
from flask_principal import (Identity,
                             identity_changed)

from application import app, lm, db
from application.flicket.forms.form_login import LogInForm
from application.flicket.models.flicket_user import FlicketUser
from application.flicket.scripts.flicket_config import set_flicket_config
from application.flicket_admin.views import admin_bp
from . import flicket_bp




# functions for redirecting user back from whence they came.
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


@lm.user_loader
def load_user(user_id):
    return FlicketUser.query.get(int(user_id))


# before any view is generated the user must be checked.
# @flicket_bp.before_request
# @admin_bp.before_request
@app.before_request
def before_request():
    set_flicket_config()
    g.user = current_user



# add 404 error handler
@app.errorhandler(403)
def not_found_error(error):
    return render_template('403.html'), 403


# add 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# handle unexpected errors
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# login page
@flicket_bp.route(app.config['WEBHOME'] + 'login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in redirect to homepage.
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('flicket_bp.index'))
    # load the LogInForm from forms.py
    form = LogInForm()

    if form.validate_on_submit():
        user = FlicketUser.query.filter_by(username=form.username.data).first()
        session['remember_me'] = form.remember_me.data
        identity_changed.send(app, identity=Identity(user.id))
        login_user(user)
        flash('You were logged in successfully.')
        return redirect(url_for('flicket_bp.index'))

    return render_template('login.html', title='Log In', form=form)


# logout page
@flicket_bp.route(app.config['WEBHOME'] + 'logout')
def logout():
    logout_user()
    flash('You were logged out successfully.')
    return redirect(url_for('flicket_bp.index'))
