#! usr/bin/python3
# -*- coding: utf8 -*-
#
# Flicket - copyright Paul Bourne: evereux@gmail.com

from flask import Flask
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_rest_jsonapi import Api
from flask_sqlalchemy import SQLAlchemy

from application.flicket.scripts.jinja2_functions import display_post_box
from application.flicket.views import flicket_bp
from application.flicket_admin.views import admin_bp
from application.flicket_api.views import flicket_api_bp

__version__ = '0.1.3b'

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)
# import jinja function
app.jinja_env.globals.update(display_post_box=display_post_box)


# Initialise Misaka for markdown
Misaka(app)

db = SQLAlchemy(app)
mail = Mail(app)
pagedown = PageDown(app)
rest_api = Api(app)

# import models so alembic can see them
from application.flicket.models import flicket_user, flicket_models
from application.flicket_admin.models import flicket_config

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'flicket_bp.login'

from .flicket_admin.views import view_admin, view_config
from .flicket.views import (assign,
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
                            markdowns,
                            release_ticket,
                            render_uploads,
                            subscribe,
                            user_edit,
                            users,
                            view)
from .flicket_api.views import api
from .flicket_api.views import rest_api

app.register_blueprint(admin_bp)
app.register_blueprint(flicket_bp)
app.register_blueprint(flicket_api_bp)