#! usr/bin/python3
# -*- coding: utf8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy

from .admin.views import admin_bp
from .flicket.views import flicket_bp
from .flicket_api.views import flicket_api_bp
from .home.views import home_bp


app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

# Initialise Misaka for markdown
Misaka(app)

db = SQLAlchemy(app)

# import models so alembic can see them
from .admin.models import user
from .flicket.models import flicket_models

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'flicket_bp.login'


from .admin.views import admin
from .flicket.views import (assign,
                            categories,
                            claim,
                            close,
                            create_ticket,
                            delete,
                            departments,
                            edit,
                            index,
                            login,
                            main,
                            markdown,
                            register,
                            release,
                            render_uploads,
                            user_edit,
                            users,
                            view)
from .flicket_api.views import api
from .home.views import views_main

app.register_blueprint(admin_bp)
app.register_blueprint(flicket_bp)
app.register_blueprint(flicket_api_bp)
app.register_blueprint(home_bp)
