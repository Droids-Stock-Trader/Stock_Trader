from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import User
from app import db
from app.auth.forms import RegistrationForm as authenticator
from flask_login import current_user
import app.validation.form_validation as validation



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

    choices=[('1', 'Email'), ('2', 'Text')]
    label = 'Contact Preference'
    val = [DataRequired()]
    contact_preference = RadioField(label,
                                    choices=choices,
                                    default='1',
                                    validators=val)
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        """ 
        Checks if the data has changed, if it has then run validation
        from app/validation
        
        Parameters
        ------
        Username -- the username to validate.
        """
        if current_user.username.lower() != username.data.lower():
            validation.validate_new_username(username)

    
    def validate_email(self, email):
        """ 
        Checks if the data has changed, if it has then run validation
        from app/validation

        Parameters
        ------
        email -- the email to validate.
        """
        if current_user.email.lower() != email.data.lower():
            validation.validate_new_email(email)

    def validate_phone_number(self, phone_number):
        """ 
        Checks if the data has changed, if it has then run validation
        from app/validation
        
        Parameters
        ------
        phone_number -- the phone number to validate.
        """
        if current_user.phone_num != phone_number.data:
            validation.validate_phone_number(phone_number)

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
