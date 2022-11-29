import datetime
from time import time
from flask import render_template, request, flash
from flask_login import current_user, login_required
from app import db
from app.stock import bp
import requests
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

    APCA_API_BASE_URL="https://paper-api.alpaca.markets"
    URI = APCA_API_BASE_URL + "/v2/positions/" + symbol
    # URI = APCA_API_BASE_URL + "/v2/orders"
    header={"ContentType":"application/x-www-form-urlencoded",'Authorization' : 'Bearer ' + current_user.get_alpaca_access_code()}
    positions = requests.get(URI,headers=header).json()
    try:
        # Used for handling empty position response
        code = positions['code']
        positions = []
    except KeyError:
        pass
    print("POSITIONS",positions)

    return render_template('stock/stock.html', title=f'{symbol} Details', stock=asset,positions=positions)


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
    append = True if request.form['append'] == 'true' else False
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
@bp.route('/create_order',methods=['POST'])
@login_required
def create_order():
        symbol = request.form['symbol']
        qty = request.form['qty']
        side = request.form['side']
        APCA_API_BASE_URL="https://paper-api.alpaca.markets"
        URI = APCA_API_BASE_URL + "/v2/orders"
        header={"ContentType":"application/x-www-form-urlencoded",'Authorization' : 'Bearer ' + current_user.get_alpaca_access_code()}
        data = {
            "symbol":symbol,
            "qty":qty,
            "side":side,
            "type":"market",
            "time_in_force":"gtc",
        }
        response = requests.post(URI,json=data,headers=header).json()
        flash("Success!")
        return response