from flask import Blueprint

import os

static_folder = os.path.join(os.getcwd(), 'application/home/static')

home_bp = Blueprint('home_bp', __name__,
                    template_folder="../templates",
                    static_folder=static_folder,
                    static_url_path='/home/static',
                    )
