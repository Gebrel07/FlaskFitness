from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from src.main.user.user import User
    return User.query.get(user_id)

