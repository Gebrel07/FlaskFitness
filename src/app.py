from flask import Flask
import json

from .extensions import bcrypt, db, login_manager


def create_app():
    app = Flask(__name__)

    app.config.from_file(filename='../config/config.json', load=json.load)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from src import _model_refs
    db.init_app(app)

    return app

