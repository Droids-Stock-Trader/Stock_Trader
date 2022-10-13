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
    title = db.Column(db.String(200))
    # Describes history log event.
    description = db.Column(db.String(3000))

    def __repr__(self):
        return f'<History: {self.title}>'
