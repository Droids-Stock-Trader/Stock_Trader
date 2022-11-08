from app import db

class News_Settings(db.Model):
    __tablename__ = 'news_settings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='news_settings')

    _TOPIC_CNT = 16
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


    @property
    def topics(self) -> list:
        """
        Returns a list of all user selected news topics 
        to search for. If all of the topics are selected
        or none of the topics are selected, returns None.
        """
        topics = []
        if self.news:
            topics.append("news")
        if self.sports:
            topics.append("sports")
        if self.tech:
            topics.append("tech")
        if self.world:
            topics.append("world")
        if self.finance:
            topics.append("finance")
        if self.politics:
            topics.append("politics")
        if self.business:
            topics.append("business")
        if self.economics:
            topics.append("economics")
        if self.entertainment:
            topics.append("entertainment")
        if self.beauty:
            topics.append("beauty")
        if self.travel:
            topics.append("travel")
        if self.music:
            topics.append("music")
        if self.food:
            topics.append("food")
        if self.science:
            topics.append("science")
        if self.gaming:
            topics.append("gaming")
        if self.energy: 
            topics.append("energy")

        if len(topics) == 0 or len(topics) == self._TOPIC_CNT:
            return None

        return topics
