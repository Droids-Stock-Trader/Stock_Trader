from app import db

class News(db.Model):
    __tablename__ = 'news'

    ID_LENGTH = 32
    CLEAN_URL_LENGTH = 128
    TITLE_LENGTH = 512
    AUTHOR_LENGTH = 128
    EXCERPT_LENGTH = 1024
    URL_LENGTH = 2046

    id = db.Column(db.String(ID_LENGTH), primary_key=True)
    title = db.Column(db.String(TITLE_LENGTH))
    author = db.Column(db.String(AUTHOR_LENGTH))
    published_date = db.Column(db.DateTime)
    link = db.Column(db.String(URL_LENGTH))
    clean_url = db.Column(db.String(CLEAN_URL_LENGTH))
    excerpt = db.Column(db.String(EXCERPT_LENGTH))
    media = db.Column(db.String(URL_LENGTH))

    