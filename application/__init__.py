import os

from flask import Flask
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy

from .home.views import home_bp
from .flicket.views import flicket_bp
from .admin.views import admin_bp

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

# Initialise Misaka for markdown
Misaka(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'flicket_bp.login'

from .home.views import views_main
from .flicket.views import (api,
                            assign,
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
from .admin.views import admin

app.register_blueprint(home_bp)
app.register_blueprint(flicket_bp)
app.register_blueprint(admin_bp)
# print(home_bp.static_folder)
# print(flicket_bp.static_folder)
