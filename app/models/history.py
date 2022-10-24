from app import db

class History(db.Model):
    """
    History Model

    Extends
    ------
    db.Model - SQLAlchemy Base Model 
    """
    __tablename__ = 'history_entry'

    # Primary key is id
    id = db.Column(db.Integer, primary_key=True)
    # Title can be up to 200 characters, not unique.
    title = db.Column(db.String(200), nullable=False)
    # Describes history log event.
    description = db.Column(db.String(3000), nullable=False)
    # Timestamp for the event
    timedata = db.Column(db.DateTime, nullable=False)
    # Foreign key of the user that owns this history log
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'<History: {self.title}>'
