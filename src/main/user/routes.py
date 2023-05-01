from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.extensions import bcrypt, db

from ..login.forms import ResetPwdForm
from .forms import EditEmailForm, EditusernameForm

user = Blueprint(
    name='user',
    import_name=__name__,
    url_prefix='/user',
    template_folder='templates'
)

@user.route('/edit-profile')
@login_required
def settings():
    return render_template('user/settings.html')

@user.route('/edit-profile/edit-username', methods=['GET', 'POST'])
@login_required
def edit_username():
    form = EditusernameForm(username=current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()

        flash('Username updated successfully!', 'alert-success')
        return redirect(url_for('user.edit_profile'))

    return render_template(
        'user/edit_username.html',
        form=form,
        return_url=url_for('user.edit_profile'),
        form_legend='Edit Username'
    )

@user.route('/edit-profile/edit-email', methods=['GET', 'POST'])
def edit_email():
    form = EditEmailForm(email=current_user.email)

    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()

        flash('Email updated successfully!', 'alert-success')
        return redirect(url_for('user.edit_profile'))
    
    return render_template(
        'user/edit_email.html',
        form=form,
        return_url=url_for('user.edit_profile'),
        form_legend='Edit Email'
    )


@user.route('/edit-profile/edit-password', methods=['GET', 'POST'])
def edit_password():
    form = ResetPwdForm()

    if form.validate_on_submit():
        new_pwd_hash = bcrypt.generate_password_hash(password=form.new_password.data)

        current_user.password = new_pwd_hash
        db.session.commit()

        flash(message='Password updated successfully!', category='alert-success')
        return redirect(url_for('user.edit_profile'))

    return render_template(
        'user/edit_password.html',
        form=form,
        return_url=url_for('user.edit_profile'),
        form_legend='Edit Password'
    )

