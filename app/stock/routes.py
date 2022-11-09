import datetime
from time import time
from flask import render_template, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app import db
from app.stock import bp
from app.models import Stock
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
# from app.stock.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm

@bp.route('/detail', methods=['GET', 'POST'])
@login_required
def stock():
    """ Stock Info Route """
    symbol = request.args.get('stock')
    asset = Stock.get_stock_info(symbol).dict()
    return render_template('stock/stock.html', title=f'{symbol} Details', stock=asset)

@bp.route('/stock_info', methods=['POST'])
@login_required
def stock_info():
    """ 
    Endpoint for processing stock info requests 
    
    HTTP Body Request Parameters
    ----------
    symbol - The symbol of stock to query
    timescale - The scale of graph to retrieve [Minute|Day|Week|Month|Year]
    """
    symbol = request.form['symbol']
    timescale = request.form['time']
    today = datetime.today()
    ts = TimeFrame.Hour
    time_delta = timedelta(hours=12)
    if (timescale == "Minute"):
        ts = TimeFrame.Minute
        time_delta = timedelta(days=3)
    elif (timescale == "Day"):
        ts = TimeFrame.Day
        time_delta = timedelta(weeks=2)
    elif (timescale == "Week"):
        ts = TimeFrame.Day
        time_delta = timedelta(weeks=4)
    elif (timescale == "Month"):
        ts = TimeFrame.Month
        time_delta = timedelta(weeks=52)
    elif (timescale == "Year"):
        ts = TimeFrame.Month
        time_delta = timedelta(weeks=52*5)

    
    yesterday = today - time_delta
    return Stock.get_stock_bars(symbol, ts, yesterday)