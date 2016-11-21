from flask import render_template, redirect, url_for, g, request, flash
from flask_login import login_required

from application import app
from application.models import User
from flicket_application.flicket_forms import SearchUserForm
from flicket_application.flicket_user_details import FlicketUserDetails


# view users
@app.route(app.config['FLICKETHOME'] + 'users/', methods=['GET', 'POST'])
@app.route(app.config['FLICKETHOME'] + 'users/<int:page>/', methods=['GET', 'POST'])
@login_required
def flicket_users(page=1):
    form = SearchUserForm()

    filter = request.args.get('filter')

    if form.validate_on_submit():
        return redirect(url_for('flicket_users', filter=form.name.data))

    users = User.query

    if filter:
        filter_1 = User.username.ilike('%{}%'.format(filter))
        filter_2 = User.name.ilike('%{}%'.format(filter))
        users = users.filter(filter_1 | filter_2)
        form.name.data = filter

    users = users.order_by(User.username.asc())
    users = users.paginate(page, app.config['POSTS_PER_PAGE'])

    return render_template('flicket/flicket_users.html',
                           title='Flicket - Users',
                           users=users,
                           form=form,
                           details=FlicketUserDetails)
