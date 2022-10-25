from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import db
from app.models import User
import app.validation.form_validation as validation


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
        """ 
        Validates that the lower case form of the username doesn't
        already exist in database.

        Parameters
        ------
        username - the username to validate.
        """
        validation.validate_new_username(username)

    def validate_email(self, email):
        """
        Validates that the lower case form of the e-mail address 
        doesn't exist in database.

        Parameters
        ------
        email - the email to validate.
        """
        validation.validate_new_email(email)


class ResetPasswordRequestForm(FlaskForm):
    """
    email -- User's email

    submit -- Submit button
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')