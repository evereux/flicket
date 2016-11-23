from flask import flash, redirect, render_template, url_for

from application import app, db
from application.admin.models.user import User
from application.flicket.forms.forms_main import RegisterForm
from application.flicket.scripts.hash_password import hash_password
from . import flicket_bp


# Register page
@flicket_bp.route(app.config['WEBHOME'] + 'register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = hash_password(form.password.data)
        register = User(username=form.username.data,
                        email=form.email.data,
                        name=form.name.data,
                        password=password)
        db.session.add(register)
        db.session.commit()
        flash('You have succesfully registered.')
        return redirect(url_for('flicket_bp.login'))
    return render_template('register.html', title='Register', form=form)
