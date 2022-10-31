from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from app import db
from app.settings import bp
from app.settings.forms import PreferencesForm, NotificationForm


@bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def user_preferences():
    """
    Updates the user preferences
       """
    if current_user.is_anonymous:
        return redirect(url_for('main.welcome'))
    form = PreferencesForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.phone_num = form.phone_number.data
        current_user.email = form.email.data
        current_user.dob = form.dob.data
        current_user.contact_pref = int(form.contact_preference.data)
        db.session.commit()
        flash("User preferences have been saved")

    form.username.data = current_user.username
    form.phone_number.data = current_user.phone_num
    form.email.data = current_user.email
    form.dob.data = current_user.dob
    form.contact_preference.data = str(current_user.contact_pref)

    return render_template('settings/preferences.html', title='User Preferences', form=form)


@bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def user_notifications():
    """
    Edit/updates user's notification settings
       """
    if current_user.is_anonymous:
        return redirect(url_for('main.welcome'))
    form = NotificationForm()

    if form.validate_on_submit():
        current_user.account_change_notify = form.account_change.data
        current_user.holds_notify = form.holds.data
        current_user.watchlist_notify = form.watchlist.data
        db.session.commit()
        flash('Notification setting have been saved.')

    form.account_change.data = current_user.account_change_notify
    form.holds.data = current_user.holds_notify
    form.watchlist.data = current_user.watchlist_notify

    return render_template('settings/notifications.html', title='Notification Settings', form=form)