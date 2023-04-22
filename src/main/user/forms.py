from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from src.extensions import db
from src.main.user.user import User


class FormSignup(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    username = StringField(validators=[DataRequired(), Length(3, 50)], render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[DataRequired(), Length(7, 50)], render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirm Password'})

    def validate_username(self, username):
        username_query = (
            db.session.query(User)
            .filter(User.username == username.data)
            .first()
        )

        if username_query:
            raise ValidationError(message='This username is unavailable')
    
    def validate_email(self, email):
        email_query = (
            db.session.query(User)
            .filter(User.email == email.data)
            .first()
        )

        if email_query:
            raise ValidationError(message='This email is unavailable')

