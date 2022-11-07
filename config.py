import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # A newscatcher api key is required for headline news. https://newscatcherapi.com/
    NEWSCATCHER_API_KEY = os.environ.get('NEWSCATCHER_API_KEY') or None
    NEWSCATCHER_API_URL = "https://api.newscatcherapi.com/v2/search"
    NEWSCATCHER_API_GEN_URL = 'https://api.newscatcherapi.com/v2/latest_headlines'
    HEADLINES_ARTICLE_CNT = 25

    # Email Configuration Variables
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = [MAIL_DEFAULT_SENDER]

    # History configurtion variables
    HISTORY_LISTING_CNT = 25
