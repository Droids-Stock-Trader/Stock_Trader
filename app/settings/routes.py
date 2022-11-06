from datetime import datetime as dt
from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from app import db
from app.settings import bp
from app.settings.forms import ProfileForm, NotificationForm, HeadlinesForm
from app.models import History


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def user_preferences():
    """
    The route that controls the user profile page.

    URL: /settings/profile
    """
    if current_user.is_anonymous:
        return redirect(url_for('main.welcome'))
    form = ProfileForm()

    if form.validate_on_submit():
        # determines what attributes have been changed
        changes_made = _profile_changed(form)
        # if changes were made
        if len(changes_made) > 0:
            # updates the user profile
            current_user.username = form.username.data
            current_user.phone_num = form.phone_number.data
            current_user.email = form.email.data
            current_user.dob = form.dob.data
            current_user.contact_pref = int(form.contact_preference.data)
            # generates the account history record 
            # and saves it to the user profile
            record = History(
                title="User Preferences Updated",
                description='The following changes were made to the ' +
                            'user profile: ' + 
                            f'{_format_changes(changes_made)}.'
            )
            current_user.store_history_record(record)
            db.session.commit()
            flash("User preferences have been saved")
    # populates the profile page with the current users attributes
    form.username.data = current_user.username
    form.phone_number.data = current_user.phone_num
    form.email.data = current_user.email
    form.dob.data = current_user.dob
    form.contact_preference.data = str(current_user.contact_pref)

    return render_template('settings/preferences.html', title='User Profile', form=form)


@bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def user_notifications():
    """
    Controller route that edits the user's 
    notification settings.

    URL: settings/notifications
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


@bp.route('/headlines', methods=['GET', 'POST'])
@login_required
def news_settings():
    form = HeadlinesForm()
    return render_template('settings/news_settings.html', title='News Settings', form=form)


def _profile_changed(form) -> bool:
    """
    Generates a list of user attributes that
    have been changed within the settings profile
    page.
    """
    changes_made = []
    if current_user.username != form.username.data:
        changes_made.append("Username")
    if current_user.phone_num != form.phone_number.data:
        changes_made.append("Phone Number")
    if current_user.email != form.email.data:
        changes_made.append("Email")
    if current_user.dob.date() != form.dob.data:
        changes_made.append("Date of Birth")
    if current_user.contact_pref != int(form.contact_preference.data):
        changes_made.append("Contact Preference")
    return changes_made


def _format_changes(changes) -> str:
    """
    Formats a list of string items to be separated by
    commas, an 'and', or both.
    """
    if len(changes) == 0:
        return ""
    elif len(changes) == 1:
        return changes[0]
    elif len(changes) == 2:
        return f'{changes[0]} and {changes[1]}'
    else:
        changes_str = ", ".join(changes[:-1])
        return changes_str + ", and " + changes[-1]
