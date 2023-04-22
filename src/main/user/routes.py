from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user

from ..user.user import User
from .forms import FormSignup

user = Blueprint(
    name='user',
    import_name=__name__,
    url_prefix='/user',
    template_folder='templates'
)

@user.route(rule='/signup', methods=['GET', 'POST'])
def signup():
    form = FormSignup()

    if form.validate_on_submit():
        user = User.create_user(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )

        login_user(user, remember=True)

        flash(message='User created successfully!', category='alert-success')

        return redirect(url_for('home.homepage'))

    return render_template('user/sign_up.html', form=form)

