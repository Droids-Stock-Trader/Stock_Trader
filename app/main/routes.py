from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import threading
import yfinance as yf
from app.main import bp

from app.models._development_data import dev_stock_data, dev_stock_dates, dev_stock_prices

@bp.route('/')
@bp.route('/index')
def index():
    """
    Default route when visiting main site.
    If user is logged in will redirect to welcome, otherwise presents dashboard.
    """
    if current_user.is_anonymous:
        return redirect(url_for('main.welcome'))
    # portfolio = dev_stock_data
    portfolio = []
    lock = threading.Lock()
    
    threads = [threading.Thread(
        target=_collect_stock_data,
        args=[stock, portfolio, lock]) 
        for stock in current_user.watch_list]

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
    stock_id = int(request.form['id'])
    data = [stock for stock in dev_stock_data if stock['id'] == stock_id][0]
    data['dates'] = dev_stock_dates
    data['prices'] = dev_stock_prices[stock_id % len(dev_stock_prices)]
    return jsonify(data)


@bp.route('/welcome')
def welcome():
    """
    Renders the welcome.html template
    """
    return render_template('main/welcome.html', title='Welcome')


def _collect_stock_data(stock, wl_data, lock) -> None:
    try:
        s = {}
        s['id'] = stock.id
        s['symbol'] = stock.symbol
        data = yf.Ticker(stock.symbol).stats()
        s['price'] = data['financialData']['currentPrice']
        s['corporate_name'] = data['price']['longName']
        s['low'] = data['summaryDetail']['dayLow']
        s['high'] = data['summaryDetail']['dayHigh']
        s['beta'] = data['defaultKeyStatistics']['beta']
        s['open'] = data['summaryDetail']['open']
        s['prev_close'] = data['summaryDetail']['previousClose']
        s['percent_change'] = round((s['price'] - s['prev_close']) * 100 / s['prev_close'], 2)
        with lock:
            wl_data.append(s)
    except:
        pass