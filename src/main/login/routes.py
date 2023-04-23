from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from markupsafe import Markup

from src.extensions import db

from ..user.user import User
from .forms import LoginForm, SignupForm

login = Blueprint(
    name='login',
    import_name=__name__,
    url_prefix=None,
    template_folder='templates'
)

@login.route(rule='/', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))

    form = LoginForm()

    if form.validate_on_submit():
        validated = User.validate_login(
            username=form.username.data,
            password=form.password.data
        )

        if validated:
            user: User = User.query.filter_by(username=form.username.data).first()

            if not user.email_confirmed:
                flash(message='Please confirm your email before logging in', category='alert-info')
                return redirect(url_for('login.login_page'))

            login_user(user=user, remember=form.remember.data)

            flash(message=Markup(f'Welcome, {user.username} &#128513;'), category='alert-success')
            return redirect(url_for(endpoint='home.homepage'))
        else:
            flash(message='Username or Password are invalid', category='alert-danger')
            return redirect(url_for('login.login_page'))

    return render_template('login/login.html', form=form)

@login.route(rule='/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User.create_user(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )

        User.send_confirmation_email(user_id=user.id)

        flash(message='The confirmation link was sent to your Email', category='alert-info')

        return redirect(url_for('login.login_page'))

    return render_template('login/sign_up.html', form=form)

@login.route(rule='/confirm-email/<int:user_id>/<token>')
def confirm_email(user_id, token):
    validated = User.validate_confirmation_token(token=token)

    if validated:
        user: User = User.query.get(user_id)
        user.email_confirmed = True
        db.session.commit()

        login_user(user)

        flash(message=f'Welcome, {user.username}', category='alert-success')
        return redirect(url_for('home.homepage'))
    else:
        abort(404)

@login.route(rule='/logout')
def logout():
    logout_user()
    return redirect(url_for('login.login_page'))

