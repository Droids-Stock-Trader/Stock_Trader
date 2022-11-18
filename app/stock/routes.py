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


@bp.route('/detail', methods=['GET', 'POST'])
@login_required
def stock():
    """ Stock Info Route """
    symbol = request.args.get('stock')    
    asset = Stock.get_stock_info(symbol).dict()
    asset['in_watch_list'] = current_user.stock_in_watch_list(asset['symbol'])
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


@bp.route('/add_to_watch_list', methods=['POST'])
@login_required
def add_remove_to_watch_list():
    """
    API call to add or remove a stock from the current
    users watchlist. 

    HTTP Body Request Parameters
    -------------
    symbol: The stocks symbol to add or remove 
    append: (0, 1) 0 to remove stock, 1 to add stock
    """
    # retrieves the request variables
    symbol = request.form['symbol']
    append = True if int(request.form['append']) == 1 else False
    try:
        # checks to see if the stock is already in the db
        # if it is not, a stock item is created
        stock = Stock.query.filter_by(symbol=symbol).first()
        if stock == None:
            asset = Stock.get_stock_info(symbol).dict()
            stock = Stock(corporate_name=asset['name'], symbol=symbol)
        # adds or removes the stock from the watch list
        if append:
            current_user.add_to_watch_list(stock)
        else:
            current_user.remove_from_watch_list(stock)    
        db.session.commit()
        return 'Success'
    except:
        db.session.rollback()
        return 'Error'