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
import yfinance as yf

class Stock(db.Model):
    __tablename__ = 'stock'

    id = db.Column(db.Integer, primary_key=True)
    corporate_name = db.Column(db.String(200))
    symbol = db.Column(db.String(25), index=True, unique=True)

    def __repr__(self):
        return f'<Stock: {self.symbol}>'

    def get_current_financial_data(self) -> dict:
        """
        Returns the current financial data from yahoo finance.

        The data is returned as a dictionary in dictionary form. For
        additional information on the keys and values format, reference
        yfinance.txt for more details.
        """
        return yf.Ticker(self.symbol).stats()
    
    def get_stock_lines(self, period='5d', interval='15m') -> dict:
        """
        Returns historical stock prices. The data is returned as a dictionary
        object with value keys, ('dates', 'prices')

        param:
            period: str
                Valid periods: 1d,5d (default),1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

            interval: str
                Valid intervals: 1m,2m,5m,15m (default),30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
        """
        # calls yahoo finance and extracts the data as a panda dataframe
        raw_data = yf.Ticker(self.symbol)
        dataframe = raw_data.history(period=period, interval=interval)
        # Extracts the used data and formats
        dates = dataframe.index
        response_data = {}
        response_data['dates'] = dates.strftime('%Y-%m-%d').tolist()
        response_data['prices'] = dataframe['Close'].values.tolist()

        return response_data

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