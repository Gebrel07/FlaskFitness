from flask import current_app, url_for
from flask_login import UserMixin
from flask_mail import Message
from itsdangerous import BadData, URLSafeTimedSerializer
from sqlalchemy import text

from src.email.email import Email
from src.extensions import bcrypt, db, mail


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=0, server_default=text('0'))

    sex = db.Column(db.Integer) # M:1, F:2 
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)

    daily_calorie_goal = db.Column(db.Float)
    
    # macro nutrients
    daily_carb_goal = db.Column(db.Float)
    daily_protein_goal = db.Column(db.Float)
    daily_fat_goal = db.Column(db.Float)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"

    @classmethod
    def create_user(
        self,
        username: str,
        password: str,
        email: str
    ):
        pwd_hash = bcrypt.generate_password_hash(password=password)

        user = self(
            username=username,
            password=pwd_hash.decode(),
            email=email
        )

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def validate_login(
        self,
        username: str,
        password: str
    ) -> bool:
        user: self = (
            db.session.query(self)
            .filter(self.username == username)
            .first()
        )

        if not user:
            return False
        
        validated = bcrypt.check_password_hash(
            pw_hash=user.password,
            password=password
        )

        return validated

    @classmethod
    def generate_confirmation_token(self, user_email: str) -> str:
        '''Generates a url safe token containing the users email'''

        serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'])

        return serializer.dumps(user_email)

    @classmethod
    def validate_confirmation_token(self, token: str):
        MAX_AGE = 600 # 10 min

        serializer = URLSafeTimedSerializer(secret_key=current_app.config['SECRET_KEY'])

        try:
            serializer.loads(s=token, max_age=MAX_AGE)
            return True
        except BadData:
            return False

    @classmethod
    def send_confirmation_email(self, user_id: int):
        user: self = self.query.get(user_id)

        token = User.generate_confirmation_token(user_email=user.email)

        link = url_for(
            'login.confirm_email',
            user_id=user_id,
            token=token,
            _external=True
        )

        email = Email()

        body = email.render_message_body(
            template=email.CONFIRM_EMAIL,
            username=user.username,
            confirmation_link=link
        )

        msg = Message(
            subject='Flask Fitness email confirmation',
            html=body,
            recipients=[user.email]
        )

        mail.send(message=msg)
        return None


