from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from markupsafe import Markup

from src.extensions import bcrypt, db

from ..user.user import User
from .forms import LoginForm, ResetPwdForm, ResetPwdTokenForm, SignupForm

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
            flash(message=Markup('Username or Password are invalid &#128542;'), category='alert-danger')
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

@login.route(rule='/reset-password', methods=['GET', 'POST'])
def send_password_reset_token():
    form = ResetPwdTokenForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            User.send_reset_pwd_email(user_id=user.id)

        flash(message='The password reset link was sent to your email', category='alert-info')
        return redirect(url_for('login.login_page'))

    return render_template('login/send_reset_token.html', form=form)

@login.route(rule='/reset-password/<int:user_id>/<token>', methods=['GET', 'POST'])
def reset_password(user_id, token):
    form = ResetPwdForm()

    validated = User.validate_confirmation_token(token=token)

    if not validated:
        abort(404)

    user: User = User.query.get(user_id)

    if not user:
        abort(404)

    if form.validate_on_submit():
        new_pwd_hash = bcrypt.generate_password_hash(password=form.new_password.data)

        user.password = new_pwd_hash
        db.session.commit()

        flash(message='Your password has been reset', category='alert-success')
        return redirect(url_for('login.login_page'))

    return render_template('login/reset_pwd.html', form=form)

