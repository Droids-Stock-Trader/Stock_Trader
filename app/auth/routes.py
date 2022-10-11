from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.models import User

# Login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is logged in here, nothing to do, return to index.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            User.username.like(form.account_identifier.data) | 
            User.email.like(form.account_identifier.data)).first()
        # If user doesn't exist or password doesn't match username
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


# Logout route
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.welcome'))

# Register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # If user is logged in, nothing to do here, return to index.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Sign Up', form=form)

# Reset password route
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # If user is logged in, nothing to do, return to index.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            pass
            # send_password_reset_email(user)
        flash('Email functionality needs to be implemented along with user email tokens to reset passwords. Need to implement within auth.reset_password_request() and email function.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)
