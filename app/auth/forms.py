from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    account_identifier = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(User.username.like(username.data)).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        elif len(username.data) > User.USERNAME_CHAR_LENGTH:
            raise ValidationError(
                f'Usernames have a maximum character length of {User.USERNAME_CHAR_LENGTH} characters.')

    def validate_email(self, email):
        user = User.query.filter(User.email.like(email.data)).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
        elif len(email.data) > User.EMAIL_CHAR_LENGTH:
            raise ValidationError(
                f'Email addresses must have a maximum length of {User.EMAIL_CHAR_LENGTH} characters.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')