#! usr/bin/python3
# -*- coding: utf8 -*-

""" Runs the application server. """

# Import app __init__.py from folder application
from application import app

# Run app with debugging turned on. This should be set to 'False' for a production environment.
# setting host to 0.0.0.0 allows external connections.
app.run(debug=True,
        host="0.0.0.0",
        port=5000,
        threaded=True,
        )
