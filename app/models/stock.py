from app import db

class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    corporate_name = db.Column(db.String(200))
    symbol = db.Column(db.String(25), index=True, unique=True)

    def __repr__(self):
        """ 
       returns the stock symbol

       """
        return f'<Stock: {self.symbol}>'
