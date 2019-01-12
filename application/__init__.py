#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import abort, Flask, g, request
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

from application.flicket.scripts.jinja2_functions import display_post_box, show_markdown
from application.flicket.views import flicket_bp
from application.flicket_admin.views import admin_bp
from application.flicket_api_v2.views import bp_api_v2
from application.flicket_errors import bp_errors

__version__ = '0.1.7'

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

# import jinja function
app.jinja_env.globals.update(display_post_box=display_post_box, show_markdown=show_markdown)

db = SQLAlchemy(app)
mail = Mail(app)
pagedown = PageDown(app)

babel = Babel(app)

# import models so alembic can see them
from application.flicket.models import flicket_user, flicket_models
from application.flicket_admin.models import flicket_config

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'flicket_bp.login'

from .flicket_admin.views import view_admin, view_config
from .flicket.views import (ticket_assign,
                            categories,
                            edit_status,
                            claim_ticket,
                            create_ticket,
                            delete,
                            departments,
                            edit,
                            history,
                            index,
                            login,
                            main,
                            faq,
                            ticket_release,
                            render_uploads,
                            subscribe,
                            user_edit,
                            users,
                            view)
from .flicket_api_v2.views import categories, departments, status, tokens, users
from .flicket_errors import handlers

app.register_blueprint(admin_bp)
app.register_blueprint(flicket_bp)
app.register_blueprint(bp_api_v2)
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
