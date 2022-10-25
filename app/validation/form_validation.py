from app.models import User
from wtforms.validators import ValidationError
from app import db
import re


def validate_new_username(username):
    """
    Validates username to fit the following requirements.
    Maximum Length < User.USERNAME_CHAR_LENGTH.
    Contains no whitespace.
    Lowercase form of username not in use.

    Parameters
    ------
    username - the username to validate.
    """
    user = User.query.filter(db.func.lower(User.username) == db.func.lower(username.data)).first()
    if user is not None:
        raise ValidationError('Please use a different username.')
    elif len(username.data) > User.USERNAME_CHAR_LENGTH:
        raise ValidationError(
            f'Usernames have a maximum character length of {User.USERNAME_CHAR_LENGTH} characters.')
    elif not username.data.find(' ') == -1:
        raise ValidationError('The username can not contain any whitespace')

def validate_new_email(email):
    """
    Validates email to fit the following requirements.
    Maximum Length < User.EMAIL_CHAR_LENGTH.
    Lowercase form of email not in use.

    Parameters
    ------
    email - the email to validate.

    """
    user = User.query.filter(db.func.lower(User.email) == db.func.lower(email.data)).first()
    if user is not None:
        raise ValidationError('Please use a different email address')
    elif len(email.data) > User.EMAIL_CHAR_LENGTH:
        raise ValidationError(
            f'Email addresses must have a maximum length of {User.EMAIL_CHAR_LENGTH} characters.')

def validate_phone_number(phone_number):
    """ 
    Checks if the data has changed, if it has then first strip valid characters, 
    and check whether length is correct and only contains numbers
    
    Parameters
    ------
    phone_number -- the phone number to validate.
    """
    stripped_number = re.sub(r"[\(\)-]","",phone_number.data)
    if (len(stripped_number) > 10):
        raise ValidationError("Phone number is too long.")
    try:
        int(stripped_number)
    except ValueError:
        raise ValidationError("Invalid characters.")
