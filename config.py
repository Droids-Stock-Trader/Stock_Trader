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
