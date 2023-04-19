from flask import Flask

from src.main.login.routes import login


def register_all_blueprints(app: Flask):
    app.register_blueprint(login)
    return None

