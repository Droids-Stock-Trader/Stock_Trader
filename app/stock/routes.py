import datetime
from time import time
from flask import render_template, request, flash, abort, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app import db
from app.stock import bp
import requests
from app.models import Stock, News, News_Settings
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from app.emails.email import send_watchlist_change_email


@bp.route('/detail', methods=['GET', 'POST'])
@login_required
def stock():
    """ Stock Info Route """
    symbol = request.args.get('stock')
    try:
        asset = Stock.get_stock_info(symbol).dict()
    except:
        flash(f'{symbol} is not a recognized stock symbol')
        return render_template(
            'stock/stock.html', 
            title=f'{symbol} Details', 
            stock={'symbol': symbol}, 
            articles=None,
            positions=None
    )
    # watchlist toggle
    asset['in_watch_list'] = current_user.stock_in_watch_list(asset['symbol'])
    # queryies the news to the stockname & stock symbol
    if current_user.news_settings == None:
        current_user.news_settings = News_Settings()
        db.session.commit()
    news_results = News.search_news_results([asset['name'], asset['symbol']], 1)
    if news_results['status_code'] != 200:
        flash(news_results['message'])
        abort(500)
    
    APCA_API_BASE_URL="https://paper-api.alpaca.markets"
    URI = APCA_API_BASE_URL + "/v2/positions/" + symbol
    # URI = APCA_API_BASE_URL + "/v2/orders"
    if (current_user.get_alpaca_access_code()):        
        header={"ContentType":"application/x-www-form-urlencoded",'Authorization' : 'Bearer ' + current_user.get_alpaca_access_code()}
        positions = requests.get(URI,headers=header).json()
    else:
        positions = {}
    try:
        # Used for handling empty position response
        code = positions['code']
        positions = []
    except KeyError:
        pass
    return render_template(
        'stock/stock.html', 
        title=f'{symbol} Details', 
        stock=asset, 
        articles=news_results['articles'],
        positions=positions
    )


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


@bp.route('/stock_summary', methods=['POST'])
@login_required
def stock_summary():
    """
    API call that returns a business summary for the given stock 
    symbol. If an error orrucs, returns 500, otherwose 200.

    param:
        symbol: The stock symbol to return the summary for.
    """
    symbol = request.form['symbol']
    stock = Stock.query.filter_by(symbol=symbol).first()
    summary = {'summary': '', 'status_code': 200}
    try:
        data = stock.get_current_financial_data()
        summary['summary'] = data['summaryProfile']['longBusinessSummary'] or None
    except:
        summary['status_code'] = 500
    return jsonify(summary)


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
        # sends an email notification of a change in the watchlist
        # if notifications are enabled for email and watchlist changes
        if (current_user.contact_pref == 1 and current_user.watchlist_notify):
            send_watchlist_change_email(current_user, append, stock)
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