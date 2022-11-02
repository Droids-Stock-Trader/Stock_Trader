from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import db
from app.models import User


class LoginForm(FlaskForm):
    """
    Login form

    account_identifier -- can be username or e-mail

    password -- User's password matching account_identifier

    remember me -- Boolean field to remember login session

    submit -- submit button
    """
    account_identifier = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """
    Registration Form

    username -- Name of the user;

    email -- User's email;

    password -- User passsword;

    password2 -- verify password;

    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """ Validates that the lower case form of the username doesn't already exist in database. """
        user = User.query.filter(db.func.lower(User.username) == db.func.lower(username.data)).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        elif len(username.data) > User.USERNAME_CHAR_LENGTH:
            raise ValidationError(
                f'Usernames have a maximum character length of {User.USERNAME_CHAR_LENGTH} characters.')
        elif not username.data.find(' ') == -1:
            raise ValidationError('The username can not contain any whitespace')

    def validate_email(self, email):
        """ Validates that the lower case form of the e-mail address doesn't exist in database. """
        user = User.query.filter(db.func.lower(User.email) == db.func.lower(email.data)).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
        elif len(email.data) > User.EMAIL_CHAR_LENGTH:
            raise ValidationError(
                f'Email addresses must have a maximum length of {User.EMAIL_CHAR_LENGTH} characters.')


class ResetPasswordRequestForm(FlaskForm):
    """
    email -- User's email

    submit -- Submit button
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Password Reset')