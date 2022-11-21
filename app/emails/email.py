from flask_mail import Message
from app import mail
from flask import render_template, current_app

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Stock Trader: Reset Your Password',
               sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html',user=user, token=token))

def send_notification_email(changes_made, user):
    for attribute in changes_made:
        send_email('Stock Trader: ' + attribute + ' Change Notification',
                   sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
                   text_body=render_template('email/notification_change.txt', user=user),
                   html_body=render_template('email/notification_change.html',user=user))

def send_password_change_email(user):
    send_email('Stock Trader: Password Change Notification',
        sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
        text_body=render_template('email/notification_change.txt', user=user),
        html_body=render_template('email/notification_change.html',user=user))

def send_notification_to_old_email(user):
    send_email('Stock Trader: Email Has Been Changed Notification',
        sender='jerry.aragon@student.csulb.edu', recipients=[user.email],
        text_body=render_template('email/notification_change.txt', user=user),
        html_body=render_template('email/notification_change.html',user=user))