from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
import datetime

followed_stocks = db.Table('followed_stocks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True)    
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    _PASSWORD_HASH_CHAR_LENGTH = 128
    USERNAME_CHAR_LENGTH = 64
    EMAIL_CHAR_LENGTH = 120
    PHONE_NUM_CHAR_LENGTH = 15

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USERNAME_CHAR_LENGTH), index=True, unique=True)
    email = db.Column(db.String(EMAIL_CHAR_LENGTH), index=True, unique=True)
    password_hash = db.Column(db.String(_PASSWORD_HASH_CHAR_LENGTH))

    phone_num = db.Column(db.String(PHONE_NUM_CHAR_LENGTH))
    dob = db.Column(db.DateTime, default=datetime.date(1,1,1))
    contact_pref = db.Column(db.Integer, default=1)

    account_change_notify = db.Column(db.Boolean, default=True)
    holds_notify = db.Column(db.Boolean, default=True)
    watchlist_notify = db.Column(db.Boolean, default=True)

    watch_list = db.relationship('Stock', secondary=followed_stocks, backref='users')
    history_list = db.relationship('History')

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def store_history_record(self, record) -> None:
        """
        Stores a history record to the User. 
        Params
        ------
        record - The History item to add to the users
        history_list.
        """
        self.history_list.append(record)

    @property
    def portfolio_corporate_names(self) -> list:
        """
        Returns a list of all of the corporate names
        of each of the stocks found within the Users
        watch list. 
        """
        return [stock.corporate_name for stock in self.watch_list]


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
