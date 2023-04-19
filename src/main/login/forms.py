from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Optional


class FormLogin(FlaskForm):
    username = StringField(render_kw={'placeholder': 'Username'}, validators=[DataRequired()])
    password = PasswordField(render_kw={'placeholder': 'Password'}, validators=[DataRequired()])
    remember = BooleanField(label='Remember', validators=[Optional()])

