from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user

from ..user.user import User
from .forms import FormLogin

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

    form = FormLogin()

    if form.validate_on_submit():
        validated = User.validate_login(
            username=form.username.data,
            password=form.password.data
        )

        if validated:
            user = User.query.filter_by(username=form.username.data).first()

            login_user(user=user, remember=form.remember.data)

            flash(message=f'Welcome, {user.username}', category='alert-success')
            return redirect(url_for(endpoint='home.homepage'))
        else:
            flash(message='Username or Password are invalid', category='alert-danger')
            return redirect(url_for('login.login_page'))
    
    return render_template('login/login.html', form=form)

