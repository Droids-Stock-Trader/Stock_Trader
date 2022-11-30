from flask_mail import Message
from app import mail
from flask import render_template, current_app

def send_email(subject, sender, recipients, text_body, html_body):
    """
    Used to send emails to a specified recipient. 
    Params
    ------
    subject - The title of the email.
    sender - The email that will be registered as the sender.
    recipients - The email who will recieve the message.
    text_body - The contents of the email in a txt format.
    html_body - The contents of the email in html format.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    """
    Sends an email to the user to reset their password.
    Params
    ------
    user - the user who will be sent the email.
    """
    token = user.get_reset_password_token()
    send_email('Stock Trader: Reset Your Password',
               sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html',user=user, token=token))

def send_notification_email(changes_made, user):
    """
    Sends a notification email for each user attribute that was changed.
    Params
    ------
    user - the user who will be sent the emails.
    """
    for attribute in changes_made:
        send_email('Stock Trader: ' + attribute + ' Change Notification',
                   sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
                   text_body=render_template('email/notification_change.txt', user=user),
                   html_body=render_template('email/notification_change.html',user=user))

def send_notifications_change_email(changes_made, user):
    """
    Sends a notification email for each user attribute that was changed.
    Params
    ------
    user - the user who will be sent the emails.
    """
    for attribute in changes_made:
        send_email('Stock Trader: ' + attribute + ' Notifications Have Been Changed',
                   sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
                   text_body=render_template('email/notification_change.txt', user=user),
                   html_body=render_template('email/notification_change.html',user=user))

def send_password_change_email(user):
    """
    Sends a notification email when the user's password is changed.
    Params
    ------
    user - the user who will be sent the email.
    """
    send_email('Stock Trader: Password Change Notification',
        sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
        text_body=render_template('email/notification_change.txt', user=user),
        html_body=render_template('email/notification_change.html',user=user))

def send_notification_to_old_email(user):
    """
    Sends a notification email to the user's 
    old email being replaced with a new email.
    Params
    ------
    user - the user who will be sent the email.
    """
    send_email('Stock Trader: Email Has Been Changed Notification',
        sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
        text_body=render_template('email/notification_change.txt', user=user),
        html_body=render_template('email/notification_change.html',user=user))

def send_watchlist_change_email(user, append, stock):
    """
    Sends a notification email to the user that
    changes have been made to their watchlist.
    Params
    ------
    user - the user who will be sent the email.
    append -  boolean which determines if a stock has been appended or removed.
    """
    if append:
        send_email('Stock Trader: ' + stock.corporate_name +' Watchlist Change Notification',
            sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
            text_body=render_template('email/add_to_watchlist.txt', user=user),
            html_body=render_template('email/add_to_watchlist.html',user=user))
    else: 
        send_email('Stock Trader: ' + stock.corporate_name + ' Watchlist Change Notification',
            sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
            text_body=render_template('email/remove_from_watchlist.txt', user=user),
            html_body=render_template('email/remove_from_watchlist.html',user=user))