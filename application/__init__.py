from flask import Flask
from flask_login import LoginManager
from flask_misaka import Misaka
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
app.config.update(TEMPLATES_AUTO_RELOAD=True)

# Initialise Misaka for markdown
Misaka(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from application import views_main, views_admin
from flicket_application import flicket_views

# todo: app initialisation checks
# does flicket upload folder exist?
