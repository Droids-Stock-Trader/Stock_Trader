from app import db
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrameUnit
from alpaca.trading.client import TradingClient
from flask import current_app, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from datetime import datetime
from flask import current_app
import requests
import urllib.parse
import json

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

    # @bp.route(('/alpaca_oauth'), methods=['GET'])
    # @login_required
    def get_account():
        APCA_API_BASE_URL="https://paper-api.alpaca.markets"
        URI = APCA_API_BASE_URL + "/v2/account"
        data = {
            'Authorization' : 'Bearer ' + current_user.get_alpaca_access_code()
        }
        response = requests.get(URI,data=data,headers={"ContentType":"application/x-www-form-urlencoded"}).json()