#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from application.flicket.views import flicket_bp
from application.flicket_admin.views import admin_bp
from application.flicket_api.views import flicket_api_bp

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

# Initialise Misaka for markdown
Misaka(app)

db = SQLAlchemy(app)
mail = Mail(app)


# import models so alembic can see them
from application.flicket.models import user, flicket_models
from application.flicket_admin.models import flicket_config

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'flicket_bp.login'

from .flicket_admin.views import view_admin, view_config
from .flicket.views import (view_assign,
                            view_categories,
                            view_change_status,
                            view_claim,
                            view_create_ticket,
                            view_delete,
                            view_departments,
                            view_edit,
                            view_index,
                            view_login,
                            view_main,
                            view_markdown,
                            view_register,
                            view_release,
                            view_render_uploads,
                            view_user_edit,
                            view_users,
                            view)
from .flicket_api.views import api

app.register_blueprint(admin_bp)
app.register_blueprint(flicket_bp)
app.register_blueprint(flicket_api_bp)
