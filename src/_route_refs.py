from flask import Flask

from src.main.home.routes import home
from src.main.login.routes import login
from src.main.user.routes import user


def register_all_blueprints(app: Flask):
    app.register_blueprint(login)
    app.register_blueprint(home)
    app.register_blueprint(user)
    return None

