from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = "login.login_page"
login_manager.login_message = "Please Log in to access this page"
login_manager.login_message_category = "alert-info"

@login_manager.user_loader
def load_user(user_id):
    from src.main.user.user import User
    return User.query.get(user_id)

