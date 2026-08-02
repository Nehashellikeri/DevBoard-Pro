from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.user import User
from app.forms.profile_forms import UpdateProfileForm, ChangePasswordForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profile():
    profile_form = UpdateProfileForm(obj=current_user)
    password_form = ChangePasswordForm()

    if profile_form.submit.data and profile_form.validate_on_submit():
        existing = User.query.filter(
            User.email == profile_form.email.data.lower(),
            User.id != current_user.id
        ).first()
        if existing:
            flash('That email is already in use by another account.', 'danger')
        else:
            current_user.name = profile_form.name.data
            current_user.email = profile_form.email.data.lower()
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))

    return render_template('profile.html', profile_form=profile_form, password_form=password_form)


@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    password_form = ChangePasswordForm()
    profile_form = UpdateProfileForm(obj=current_user)

    if password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
        return redirect(url_for('profile.view_profile'))

    return render_template('profile.html', profile_form=profile_form, password_form=password_form)
