from datetime import datetime as dt
import random
import string
from flask import current_app, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
import requests
import urllib.parse
from app import db
from app.settings import bp
from app.settings.forms import ProfileForm, NotificationForm, HeadlinesForm
from app.models import History, News_Settings
from app.emails.email import send_notification_email


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def user_preferences():
    """
    The route that controls the user profile page.

    URL: /settings/profile
    """
    form = ProfileForm()
    if form.validate_on_submit():
        # determines what attributes have been changed and
        # assings the changed values to the current users db
        changes_made = _profile_changed(form)
        # if changes were made
        if len(changes_made) > 0:
            # generates the account history record
            # and saves it to the user profile
            record = History(
                title="User Profile Updated",
                description='The following changes were made to the ' +
                    f'user profile: {_format_changes(changes_made)}.'
            )
            current_user.store_history_record(record)
            db.session.commit()
            # sends a notification email based on the attributes changed
            # if the contact preference is set to email and notifications are turned on
            if (current_user.contact_pref == 1 and current_user.account_change_notify):
                send_notification_email(changes_made, current_user)
            flash("User profile have been saved")
    # populates the profile page with the current users attributes
    _populate_profile_form(form)
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
    form = NotificationForm()
    if form.validate_on_submit():
        # generates a list of notification settings that have been changed
        # and updates the user notification settings.
        changes_made = _notification_changes(form)
        if len(changes_made) > 0:
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
    _populate_notification_form(form)
    return render_template(
        'settings/notifications.html', 
        title='Notification Settings', form=form)


@bp.route('/brokers', methods=['GET'])
@login_required
def brokers_settings():
    """
    Controller route that edits the user's
    broker settings.
    
    URL: settings/brokers
    """
    if current_user.get_alpaca_access_code():
        connected = True
    else:
        connected = False
    return render_template('settings/brokers.html',title="Broker settings",connected=connected, code=current_user.get_alpaca_access_code())

@bp.route(('/connect_alpaca'), methods=['GET'])
@login_required
def connect_alpaca():
    BASE_URL = "http://127.0.0.1:5000"
    CLIENT_ID = current_app.config["ALPACA_CLIENT_ID"]
    RANDOM_STATE = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
    UNENCODED_REDIRECT_URI = BASE_URL + url_for('settings.alpaca_code')
    REDIRECT_URI = urllib.parse.quote_plus(UNENCODED_REDIRECT_URI)
    URI = f"https://app.alpaca.markets/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=account:write%20trading"
    return redirect(URI)

@bp.route(('/alpaca_oauth'), methods=['GET'])
@login_required
def alpaca_code():
    CLIENT_ID = current_app.config["ALPACA_CLIENT_ID"]
    SECRET_ID = current_app.config["ALPACA_SECRET_ID"]
    BASE_URL = "http://127.0.0.1:5000"
    UNENCODED_REDIRECT_URI = BASE_URL + url_for('settings.alpaca_code')
    REDIRECT_URI = urllib.parse.quote_plus(UNENCODED_REDIRECT_URI)
    code = request.args.get('code')
    URI = "https://api.alpaca.markets/oauth/token"
    data = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'client_id' : CLIENT_ID,
        'client_secret' : SECRET_ID,
        'redirect_uri' : UNENCODED_REDIRECT_URI
    }
    response = requests.post(URI,data=data,headers={"ContentType":"application/x-www-form-urlencoded"}).json()
    access_token = response['access_token']
    current_user.set_alpaca_access_code(access_token)
    db.session.commit()
    if (len(access_token) > 0):
        flash("Successfully connected brokerage account.")
    else:
        flash("Something went wrong.",category='error')
    return redirect(url_for('settings.brokers_settings'))

@bp.route(('/disconnect_alpaca'), methods=['GET'])
@login_required
def disconnect_alpaca():
    current_user.set_alpaca_access_code(None)
    db.session.commit()
    return redirect(url_for('settings.brokers_settings'))


@bp.route('/headlines', methods=['GET', 'POST'])
@login_required
def news_settings():
    """
    Controller route that edits the user's 
    news settings.

    URL: settings/headlines
    """
    # Check to see if the current user does not has a news settings 
    # table already assigned. Assigns a table if none exits.
    if current_user.news_settings == None:
        current_user.news_settings = News_Settings()
        db.session.commit()    
    form = HeadlinesForm()
    if form.validate_on_submit():
        # get the news settings changes and
        # assigns the form value to the users db
        changes_made = _news_changes(form)
        # if changes were made to 1 or more settings
        if len(changes_made) > 0:
            record = History(
                title='News Settings Updated',
                description='The following news settings were changed: ' +
                    f'{_format_changes(changes_made)}.'
            )
            current_user.store_history_record(record)
            db.session.commit()
            flash("News settings updated.")
    # populates the form to the current users news settings
    _populate_news_form(form)
    return render_template(
        'settings/news_settings.html', title='News Settings', form=form)


def _profile_changed(form: ProfileForm) -> list:
    """
    Generates a list of user attributes that
    have been changed within the settings profile
    page. If the value has changed, the form value 
    is assigned to the current users profile settings.

    Params
    ------
    form - The profile settings form containing the updated data.
    """
    changes = []
    if current_user.username != form.username.data:
        changes.append("Username")
        current_user.username = form.username.data
    if current_user.phone_num != form.phone_number.data:
        changes.append("Phone Number")
        current_user.phone_num = form.phone_number.data
    if current_user.email != form.email.data:
        changes.append("Email")
        current_user.email = form.email.data
    if current_user.dob == None:
        if form.dob.data != None:
            changes.append("Date of Birth")
            current_user.dob = form.dob.data
    elif current_user.dob.date() != form.dob.data:
        changes.append("Date of Birth")
        current_user.dob = form.dob.data
    if current_user.contact_pref != int(form.contact_preference.data):
        changes.append("Contact Preference")
        current_user.contact_pref = int(form.contact_preference.data)
    return changes


def _notification_changes(form: NotificationForm) -> list:
    """
    Generates a list of user notification settings
    that have been changed within the notifications
    settings page. If the setting has changed, the form
    value is assinged to the users notification settings.

    Params
    ------
    form - The notification settings form containing the updated data.
    """
    changes = []
    if current_user.account_change_notify != form.account_change.data:
        changes.append("Account Profile")
        current_user.account_change_notify = form.account_change.data
    if current_user.holds_notify != form.holds.data:
        changes.append("Holdings")
        current_user.holds_notify = form.holds.data
    if current_user.watchlist_notify != form.watchlist.data:
        changes.append("Account Portfolio")
        current_user.watchlist_notify = form.watchlist.data
    return changes


def _news_changes(form: HeadlinesForm) -> list:
    """
    Generates a list of user news settings that
    have been changed within the news settings page.
    If a change was made, the current users attribute
    is updated with the new form value.

    Params
    ------
    form - The news settings form containing the updated data.
    """
    ns = current_user.news_settings
    changes = []
    if ns.news != form.news.data:
        ns.news = form.news.data
        changes.append("News")
    if ns.sports != form.sports.data:
        ns.sports = form.sports.data
        changes.append("Sports")
    if ns.tech != form.tech.data:
        ns.tech = form.tech.data
        changes.append("Tech")
    if ns.world != form.world.data:
        ns.world = form.world.data
        changes.append("World")
    if ns.finance != form.finance.data:
        ns.finance = form.finance.data
        changes.append("Finance")
    if ns.politics != form.politics.data:
        ns.politics = form.politics.data
        changes.append("Politics")
    if ns.business != form.business.data:
        ns.business = form.business.data
        changes.append("Business")
    if ns.economics != form.economics.data:
        ns.economics = form.economics.data
        changes.append("Economics")
    if ns.entertainment != form.entertainment.data:
        ns.entertainment = form.entertainment.data
        changes.append("Entertainment")
    if ns.beauty != form.beauty.data:
        ns.beauty = form.beauty.data
        changes.append("Beauty")
    if ns.travel != form.travel.data:
        ns.travel = form.travel.data
        changes.append("Travel")
    if ns.music != form.music.data:
        ns.music = form.music.data
        changes.append("Music")
    if ns.food != form.food.data:
        ns.food = form.food.data
        changes.append("Food")
    if ns.science != form.science.data:
        ns.science = form.science.data
        changes.append("Science")
    if ns.gaming != form.gaming.data:
        ns.gaming = form.gaming.data
        changes.append("Gaming")
    if ns.energy != form.energy.data:
        ns.energy = form.energy.data
        changes.append("Energy")    
    return changes


def _populate_profile_form(form: ProfileForm) -> None:
    """
    Populates the given ProfileForm with the 
    current users news settings.

    Params
    ------
    form - The ProfileForm to populate.
    """
    form.username.data = current_user.username
    form.phone_number.data = current_user.phone_num
    form.email.data = current_user.email
    form.dob.data = current_user.dob
    form.contact_preference.data = str(current_user.contact_pref)


def _populate_notification_form(form: NotificationForm) -> None:
    """
    Populates the given NotificationForm with the 
    current users news settings.

    Params
    ------
    form - The NotificationForm to populate.
    """
    form.account_change.data = current_user.account_change_notify
    form.holds.data = current_user.holds_notify
    form.watchlist.data = current_user.watchlist_notify


def _populate_news_form(form: HeadlinesForm) -> None:
    """
    Populates the given HeadlinesForm with the 
    current users news settings.

    Params
    ------
    form - The HeadlinesForm to populate.
    """
    ns = current_user.news_settings
    form.news.data = ns.news
    form.sports.data = ns.sports
    form.tech.data = ns.tech
    form.world.data = ns.world
    form.finance.data = ns.finance
    form.politics.data = ns.politics
    form.business.data = ns.business
    form.economics.data = ns.economics
    form.entertainment.data = ns.entertainment
    form.beauty.data = ns.beauty
    form.travel.data = ns.travel
    form.music.data = ns.music
    form.food.data = ns.food
    form.science.data = ns.science
    form.gaming.data = ns.gaming
    form.energy.data = ns.energy


def _format_changes(changes: list) -> str:
    """
    Formats a list of string items to be separated by
    commas, an 'and', or both.

    Params
    ------
    changes - List of string items to format.
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
