import json
import os

from flask import Flask

from ._route_refs import register_all_blueprints
from .extensions import bcrypt, db, login_manager, mail, migrate

# TODO: create reset password page
# TODO: create search, add and edit food pages
# TODO: create track calories page (add, edit and remove items from daily cal number)
# TODO: create dashboard for home page (show current status of daily goals, use chart js)


def create_app():
    app = Flask(__name__)

    app.config.from_file(filename='../configs/config.json', load=json.load)
    app.config.from_file(filename='../configs/email.json', load=json.load)

    app.template_folder = os.path.join(
        app.root_path,
        app.config.get('TEMPLATE_FOLDER')
    )
    app.static_folder = app.config.get('STATIC_FOLDER')

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from src import _model_refs
    db.init_app(app)

    migrate.init_app(app, db)

    mail.init_app(app)

    register_all_blueprints(app=app)

    return app

