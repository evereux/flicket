import os
from urllib.parse import urlparse, urljoin

import bcrypt
from flask import (flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   url_for,
                   session,
                   send_from_directory)
from flask_login import (login_user,
                         logout_user,
                         current_user,
                         login_required)
from flask_principal import (Identity,
                             identity_changed,
                             identity_loaded,
                             Permission,
                             Principal,
                             RoleNeed,
                             UserNeed,
                             )

from application import app, db, lm
from .models import User
from .forms import LogInForm, RegisterForm, EditUserForm
from .functions_login import check_password_format

principals = Principal(app)
# define admin role need
admin_only = RoleNeed('admin')
admin_permission = Permission(admin_only)


# used for debugging purposes only
def print_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            print("Error in the {} field - {}".format(
                getattr(form, field).label.text,
                error
            ))


# functions for redirecting user back from whence they came.
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# before any view is generated the user must be checked.
@app.before_request
def before_request():
    g.user = current_user


# add 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# handle unexpected errors
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


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
    if hasattr(current_user, 'groups'):
        the_user = User.query.filter_by(id=current_user.id).first()
        for g in the_user.groups:
            identity.provides.add(RoleNeed('{}'.format(g.group_name)))


# index page
@app.route(app.config['WEBHOME'])
def index():
    query = User.query.all()
    return render_template('index.html', title='Flicket Ticket System')


# login page
@app.route(app.config['WEBHOME'] + 'login', methods=['GET', 'POST'])
def login():
    # if the user is already logged in redirect to homepage.
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    # load the LogInForm from forms.py
    form = LogInForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session['remember_me'] = form.remember_me.data
        identity_changed.send(app, identity=Identity(user.id))
        login_user(user)
        flash('You were logged in successfully.')
        return redirect(url_for('index'))

    return render_template('login.html', title='Log In', form=form)


# logout page
@app.route(app.config['WEBHOME'] + 'logout')
def logout():
    logout_user()
    flash('You were logged out successfully.')
    return redirect(url_for('index'))


# Register page
@app.route(app.config['WEBHOME'] + 'register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = form.password.data
        password = password.encode('utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt())
        register = User(username=form.username.data,
                        email=form.email.data,
                        name=form.name.data,
                        password=password)
        db.session.add(register)
        db.session.commit()
        flash('You have succesfully registered.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# a typical page the requires a user to be logged in.
@app.route(app.config['WEBHOME'] + 'logged_in_user', methods=['GET', 'POST'])
@login_required
def logged_in_user():
    return render_template('logged_in_user.html', title='Logged In Users Only')


# edit self page
@app.route(app.config['WEBHOME'] + 'user_details', methods=['GET', 'POST'])
@login_required
def user_details():
    form = EditUserForm()

    if form.validate_on_submit():

        # find the user in db to edit
        user = User.query.filter_by(id=g.user.id).first()
        user.name = form.name.data
        user.email = form.email.data
        flash('You have edited your user details.', category='success')

        password = form.new_password.data
        if (password != '') and (check_password_format(password)):
            password = password.encode('utf-8')
            password = bcrypt.hashpw(password, bcrypt.gensalt())
            user.password = password
            flash('You have changed your password.', category='success')

        db.session.commit()

        return redirect(url_for('user_details'))

    form.name.data = g.user.name
    form.email.data = g.user.email
    form.username.data = g.user.username

    return render_template('edit_user.html', form=form, title='Edit User Details')


# return images
@app.route(app.config['WEBHOME'] + 'flicket_uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def view_ticket_uploads(filename):
    path = os.path.join(os.getcwd(), app.config['TICKET_UPLOAD_FOLDER'])
    return send_from_directory(path, filename)


@app.route(app.config['WEBHOME'] + 'dropzone', methods=['GET', 'POST'])
@login_required
def dropzone():
    return render_template('dropzone.html')