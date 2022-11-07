from app import db

class News_Settings(db.Model):
    __tablename__ = 'news_settings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='news_settings')

    news = db.Column(db.Boolean, default=True, nullable=False)
    sports = db.Column(db.Boolean, default=True, nullable=False)
    tech = db.Column(db.Boolean, default=True, nullable=False)
    world = db.Column(db.Boolean, default=True, nullable=False)
    finance = db.Column(db.Boolean, default=True, nullable=False)
    politics = db.Column(db.Boolean, default=True, nullable=False)
    business = db.Column(db.Boolean, default=True, nullable=False)
    economics = db.Column(db.Boolean, default=True, nullable=False)
    entertainment = db.Column(db.Boolean, default=True, nullable=False)
    beauty = db.Column(db.Boolean, default=True, nullable=False)
    travel = db.Column(db.Boolean, default=True, nullable=False)
    music = db.Column(db.Boolean, default=True, nullable=False)
    food = db.Column(db.Boolean, default=True, nullable=False)
    science = db.Column(db.Boolean, default=True, nullable=False)
    gaming = db.Column(db.Boolean, default=True, nullable=False)
    energy = db.Column(db.Boolean, default=True, nullable=False)
