#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

"""

    Flicket
    =======

    A simple ticket system using Python and the Flask microframework.

    This probably wouldn't have been created without the excellent tutorials written by Miguel Grinberg:
    https://blog.miguelgrinberg.com. Many thanks kind sir.


"""

from flask import abort
from flask import Flask
from flask import g
from flask import request
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

from application.flicket_admin.views import admin_bp
from application.flicket_api.views import bp_api
from application.flicket_errors import bp_errors
from application.flicket.views import flicket_bp
from application.flicket.scripts.jinja2_functions import display_post_box
from application.flicket.scripts.jinja2_functions import now_year
from application.flicket.scripts.jinja2_functions import show_markdown

__version__ = '0.2.0'

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

db = SQLAlchemy(app)
mail = Mail(app)
pagedown = PageDown(app)

babel = Babel(app)

# import jinja function
app.jinja_env.globals.update(display_post_box=display_post_box, show_markdown=show_markdown, now_year=now_year)

# import models so alembic can see them
from application.flicket.models import flicket_user, flicket_models
from application.flicket_admin.models import flicket_config

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'flicket_bp.login'

from .flicket_admin.views import view_admin
from .flicket_admin.views import view_config
from .flicket_admin.views import view_email_test

from .flicket.views import ticket_assign
from .flicket.views import categories
from .flicket.views import edit_status
from .flicket.views import ticket_claim
from .flicket.views import ticket_create
from .flicket.views import delete
from .flicket.views import departments
from .flicket.views import edit
from .flicket.views import history
from .flicket.views import index
from .flicket.views import login
from .flicket.views import help
from .flicket.views import tickets
from .flicket.views import ticket_release
from .flicket.views import render_uploads
from .flicket.views import subscribe
from .flicket.views import user_edit
from .flicket.views import users
from .flicket.views import ticket_view

from .flicket_api.views import actions
from .flicket_api.views import categories
from .flicket_api.views import departments
from .flicket_api.views import histories
from .flicket_api.views import posts
from .flicket_api.views import priorities
from .flicket_api.views import status
from .flicket_api.views import subscriptions
from .flicket_api.views import tickets
from .flicket_api.views import tokens
from .flicket_api.views import uploads
from .flicket_api.views import users

from .flicket_errors import handlers

app.register_blueprint(admin_bp)
app.register_blueprint(flicket_bp)
app.register_blueprint(bp_api)
app.register_blueprint(bp_errors)


# prints url routes for debugging
# for rule in app.url_map.iter_rules():
#    print(rule)


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if hasattr(user, 'locale'):
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en in this
    # example.  The best match wins.
    return request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'].keys())


@app.url_defaults
def set_language_code(endpoint, values):
    if 'lang_code' in values or not g.get('lang_code', None):
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code


@app.url_value_preprocessor
def get_lang_code(endpoint, values):
    if values is not None:
        g.lang_code = values.pop('lang_code', None)


@app.before_request
def ensure_lang_support():
    lang_code = g.get('lang_code', None)
    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
        return abort(404)
