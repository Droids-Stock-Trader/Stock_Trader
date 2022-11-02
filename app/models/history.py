from app import db
from datetime import datetime as dt

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
    # UTC timestamp for the event
    timedata = db.Column(db.DateTime, nullable=False)
    # Foreign key of the user that owns this history log
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, **kwargs):
        """
        Default constructor for a History item.
        If a timedata kwargs is not given, timedata
        will be set to the current UTC time.
        """
        super(History, self).__init__(**kwargs)
        if not 'timedata' in kwargs:
            self.timedata = dt.utcnow()

    def __repr__(self):
        return f'<History: {self.title}>'