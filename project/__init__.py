# project/__init__.py


import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# instantiate the database
db = SQLAlchemy()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')  # pull in environment variables
    app.config.from_object(app_settings) # set configuration from config.py

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
