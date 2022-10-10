from app import db

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(512))
    author = db.Column(db.String(128))
    published_date = db.Column(db.DateTime)
    link = db.Column(db.String(2046))
    clean_url = db.Column(db.String(128))
    excerpt = db.Column(db.String(1024))
    media = db.Column(db.String(2046))