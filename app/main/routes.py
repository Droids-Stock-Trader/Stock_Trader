from datetime import datetime as dt, timedelta
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import threading
from app.main import bp
from app.models.stock import Stock

from app.models._development_data import dev_stock_data, dev_stock_dates, dev_stock_prices

@bp.route('/')
@bp.route('/index')
def index():
    """
    Default route when visiting the site.
    If user is not logged in, the user will be redirect to the 
    welcome page.
    """
    if current_user.is_anonymous:
        return redirect(url_for('main.welcome'))
    # Collects all of the stocks found within the users watchlist
    # and creates a function thead to collect the all of the data
    # concurrently. 
    portfolio = []
    lock = threading.Lock()    
    threads = [threading.Thread(
        target=_collect_stock_data,
        args=[stock, portfolio, lock]) 
        for stock in current_user.watch_list]
    # starts each thread and waits for all theads to complete before continuing.
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return render_template('main/index.html', title='Dashboard', portfolio=portfolio)


@bp.route('/query_stock_info', methods=['POST'])
@login_required
def query_stock_info():
    """
    Makes an HTTPS POST request for information on a stock
    """
    # this all needs to be rewritten to use the db and to do proper error checking
    symbol = request.form['symbol']
    
    delta = timedelta(days=-7)
    date_end = dt.now()
    date_start = date_end + delta

    
    
    # data = [stock for stock in dev_stock_data if stock['id'] == stock_id][0]
    data = [stock for stock in dev_stock_data if stock['id'] == 1][0]   # TODO - Needs to go.
    
    
    data['dates'] = dev_stock_dates
    data['prices'] = dev_stock_prices[0]
    return jsonify(data)


@bp.route('/welcome')
def welcome():
    """
    Renders the welcome.html template
    """
    return render_template('main/welcome.html', title='Welcome')


def _collect_stock_data(
    stock: Stock, 
    wl_data: list, 
    lock: threading.Lock) -> None:
    """
    Appends the given stock financial details to the
    given watchlist. This function is meant to be called
    concurrently with other functions that have write
    to the given watchlist. A lock must be provided to the
    finantial data to be appended to the watchlist.

    param:
        stock: The stock object that is to be added to the 
        to the watch list. The stock must have already been
        commited to the db requiring an assigned id.
        
        wl_data: The watch list to assign the stock data to.
        
        lock: The treading lock to prevent writing errors to
        watchlist.
    """
    try:
        s = {}
        s['id'] = stock.id
        s['symbol'] = stock.symbol
        data = stock.get_current_financial_data()
        s['low'] = data['summaryDetail']['dayLow'] or None
        s['high'] = data['summaryDetail']['dayHigh'] or None
        s['beta'] = data['defaultKeyStatistics']['beta'] or None
        s['open'] = data['summaryDetail']['open'] or None
        s['price'] = data['financialData']['currentPrice'] or None
        s['prev_close'] = data['summaryDetail']['previousClose'] or None
        s['corporate_name'] = data['price']['longName'] or None
        s['percent_change'] = round(
            (s['price'] - s['prev_close']) * 100 / s['prev_close'], 2) or None
        with lock:
            wl_data.append(s)
    except:
        pass