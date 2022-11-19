from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from time import time
import jwt
from flask import current_app
from app.models.stock import Stock


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
    dob = db.Column(db.DateTime)
    contact_pref = db.Column(db.Integer, default=1)

    account_change_notify = db.Column(db.Boolean, default=True)
    holds_notify = db.Column(db.Boolean, default=True)
    watchlist_notify = db.Column(db.Boolean, default=True)

    watch_list = db.relationship('Stock', secondary=followed_stocks, backref='users')
    history_list = db.relationship('History')
    news_settings = db.relationship(
        'News_Settings', back_populates='user', 
        uselist=False, lazy=True
    )

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

    def stock_in_watch_list(self, symbol: str) -> bool:
        '''
        Checks whether or not a stock is currently in the
        users watchlist. 

        param:
            symbol: The stock symbol of the stock to search for.

        return:
            bool: True if the stock is in the users watchlist, otherwise False
        '''
        for s in self.watch_list:
            if s.symbol.upper() == symbol.upper():
                return True
        return False

    def add_to_watch_list(self, stock) -> None:
        '''
        Adds the given stock to the users watchlist 

        param:
            stock: The Stock item to add to the users watchlist
        '''
        s = Stock.query.filter_by(symbol=stock.symbol).first()
        if s == None:
            self.watch_list.append(stock)
        else:
            self.watch_list.append(s)
    
    def remove_from_watch_list(self, stock) -> None:
        '''
        removes the given stock to the users watchlist 

        param:
            stock: The Stock item to remove from the users watchlist
        '''
        if self.stock_in_watch_list(stock.symbol):
            for i, s in enumerate(self.watch_list):
                if s.symbol == stock.symbol:
                    self.watch_list.pop(i)
                    break

    @property
    def portfolio_corporate_names(self) -> list:
        """
        Returns a list of all of the corporate names
        of each of the stocks found within the Users
        watch list. 
        """
        return [stock.corporate_name for stock in self.watch_list]

    def get_reset_password_token(self, expires_in=600):
        '''
        Returns a JWT token as a string, which is 
        generated directly by the jwt.encode() function        
        '''
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        """
        This method takes a token and attempts to decode it. 
        If the token cannot be validated, an exception will be raised, 
        which is caught and 'none' is returned. If the token is valid, then the 
        value of the reset_password key from the token's payload is 
        the ID of the user, which can load the user and return it.
        """
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
