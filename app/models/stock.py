from app import db
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import AssetClass
from datetime import datetime
from flask import current_app
import json
import os

class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    corporate_name = db.Column(db.String(200))
    symbol = db.Column(db.String(25), index=True, unique=True)

    def __repr__(self):
        return f'<Stock: {self.symbol}>'

    @staticmethod
    def get_stock_bars(symbol, Unit : TimeFrameUnit, start_datetime : datetime):
        """
        Used to query a stock for price and history data.

        Parameters
        ----------
        symbol - stock symbol.
        Unit - Timeframe for bars to cover.
        start_datetime - How far into the past the data requested should go.
        """
        ALPACA_API_KEY = current_app.config["ALPACA_API_KEY"]
        ALPACA_SECRET_KEY = current_app.config["ALPACA_SECRET_KEY"]
        client = StockHistoricalDataClient(ALPACA_API_KEY,ALPACA_SECRET_KEY)

        request_params = StockBarsRequest(
                            symbol_or_symbols=[symbol],
                            timeframe=Unit,
                            start=start_datetime)
        bars = client.get_stock_bars(request_params)
        bars_df = bars.df
        return json.loads(bars.json())

    @staticmethod
    def get_stock_info(symbol):
        """
        Method for retrieving basic information about a stock such as name,
        symbol, and status.  Not for price/history data.
        """
        ALPACA_API_KEY = current_app.config["ALPACA_API_KEY"]
        ALPACA_SECRET_KEY = current_app.config["ALPACA_SECRET_KEY"]
        trading_client = TradingClient(ALPACA_API_KEY,ALPACA_SECRET_KEY)
        asset = trading_client.get_asset(symbol_or_asset_id=symbol)
        return asset