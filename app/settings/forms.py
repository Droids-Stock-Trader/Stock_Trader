from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User
from app import db
from app.auth.forms import RegistrationForm as authenticator
from flask_login import current_user
import re



class PreferencesForm(FlaskForm):
    """ 
    Form for user viewing and editting their preferences. 
    
    Extends
    -------
    FlaskForm
    """
    username = StringField('Username', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date Of Birth')
    contact_preference = RadioField('Contact Preference', choices=[('1', 'Email'), ('2', 'Text')], default='1', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        """ 
        Checks if the data has changed, if it has then run validation from app/auth/RegistrationForm
        
        Parameters
        ------
        Username -- the username to validate.
        """
        if current_user.username.lower() != username.data.lower():
            authenticator.validate_username(self, username)

    
    def validate_email(self, email):
        """ 
        Checks if the data has changed, if it has then run validation from app/auth/RegistrationForm

        Parameters
        ------
        email -- the email to validate.
        """
        if current_user.email.lower() != email.data.lower():
            authenticator.validate_email(self, email)

    def validate_phone_number(self, phone_number):
        """ 
        Checks if the data has changed, if it has then first strip valid characters, 
        and check whether length is correct and only contains valid characters
        
        Parameters
        ------
        phone_number -- the phone number to validate.
        """
        if current_user.phone_num != phone_number.data:
            stripped_number = re.sub(r"[\(\)-]","",phone_number.data)
            if (len(stripped_number) > 10):
                raise ValidationError("Phone number is too long.")
            if not (isinstance(eval(stripped_number), int)):
                raise ValidationError("Invalid characters.")

class NotificationForm(FlaskForm):
    """ 
    Form for user viewing and editting their notifications. 
    
    Extends
    ------
    FlaskForm
    """
    account_change = BooleanField('Account Changes')
    holds = BooleanField('Holdings')
    watchlist = BooleanField('Watch List', default='checked')
    submit = SubmitField('Save Changes')
