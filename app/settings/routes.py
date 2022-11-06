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
                title="User Profile Updated",
                description='The following changes were made to the ' +
                    f'user profile: {_format_changes(changes_made)}.'
            )
            current_user.store_history_record(record)
            db.session.commit()
        flash("User profile have been saved")
    # populates the profile page with the current users attributes
    form.username.data = current_user.username
    form.phone_number.data = current_user.phone_num
    form.email.data = current_user.email
    form.dob.data = current_user.dob
    form.contact_preference.data = str(current_user.contact_pref)

    return render_template(
        'settings/preferences.html', title='User Profile', form=form)


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
        # generates a list of notification settings that have been changed.
        changes_made = _notification_changes(form)
        if len(changes_made) > 0:
            # Updates the user attributes
            current_user.account_change_notify = form.account_change.data
            current_user.holds_notify = form.holds.data
            current_user.watchlist_notify = form.watchlist.data
            # Creates a record of what was changed and saves the record 
            # to the users account history.
            record = History(
                title='Notification Settings Updated',
                description='The following notification settings ' + 
                    f'changed: {_format_changes(changes_made)}.'
            )
            current_user.store_history_record(record)
            db.session.commit()
        flash('Notification setting have been saved.')
    # populates the notification page with the current user notification settings
    form.account_change.data = current_user.account_change_notify
    form.holds.data = current_user.holds_notify
    form.watchlist.data = current_user.watchlist_notify

    return render_template(
        'settings/notifications.html', 
        title='Notification Settings', form=form)


@bp.route('/headlines', methods=['GET', 'POST'])
@login_required
def news_settings():
    form = HeadlinesForm()
    return render_template(
        'settings/news_settings.html', title='News Settings', form=form)


def _profile_changed(form) -> list:
    """
    Generates a list of user attributes that
    have been changed within the settings profile
    page.
    """
    changes = []
    if current_user.username != form.username.data:
        changes.append("Username")
    if current_user.phone_num != form.phone_number.data:
        changes.append("Phone Number")
    if current_user.email != form.email.data:
        changes.append("Email")
    if current_user.dob.date() != form.dob.data:
        changes.append("Date of Birth")
    if current_user.contact_pref != int(form.contact_preference.data):
        changes.append("Contact Preference")
    return changes


def _notification_changes(form) -> list:
    """
    Generates a list of user notification settings
    that have been changed within the notifications
    settings page.
    """
    changes = []
    if current_user.account_change_notify != form.account_change.data:
        changes.append("Account Profile")
    if current_user.holds_notify != form.holds.data:
        changes.append("Holdings")
    if current_user.watchlist_notify != form.watchlist.data:
        changes.append("Account Portfolio")
    return changes


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
