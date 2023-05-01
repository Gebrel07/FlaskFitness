from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from src.extensions import db

from .user import User


class EditusernameForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(3, 50)], render_kw={'placeholder': 'New Username'})

    def validate_username(self, username):
        if username.data == current_user.username:
            raise ValidationError('New username cannot be the same as current one')
        else:
            query = (
                db.session.query(User)
                .filter(User.username == username.data)
                .first()
            )

            if query:
                raise ValidationError(message='This username is unavailable')


class EditEmailForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    confirm_email = EmailField(validators=[DataRequired(), Email(), EqualTo('email', 'Must be equal to Email')], render_kw={'placeholder': 'Confirm Email'})

    def validate_email(self, email):
        if email.data == current_user.email:
            raise ValidationError('New email cannot be the same as current one')
        else:
            email_query = (
                db.session.query(User)
                .filter(User.email == email.data)
                .first()
            )

            if email_query:
                raise ValidationError(message='This email is unavailable')

