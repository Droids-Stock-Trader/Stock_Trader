from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
import threading
from app.main import bp
from app.models.stock import Stock


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
    stock_id = request.form['id']
    stock = Stock.query.get(stock_id)

    stock_data = []
    lock = threading.Lock()
    args = [stock, stock_data, lock]
    stats_thread = threading.Thread(target=_collect_stock_data, args=args)
    graph_thread = threading.Thread(target=_collect_graph_data, args=args)
    stats_thread.start()
    graph_thread.start()
    stats_thread.join()
    graph_thread.join()

    response_data = {**stock_data[0], **stock_data[1]}

    return jsonify(response_data)


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
    financial data to be appended to the watchlist.

    param:
        stock: The stock object that is to be added to the 
        to the watch list. The stock must have already been
        committed to the db requiring an assigned id.
        
        wl_data: The watch list to assign the stock data to.
        
        lock: The treading lock to prevent writing errors to
        watchlist.
    """
    s = {}
    try:
        s['id'] = stock.id
        s['symbol'] = stock.symbol
        data = stock.get_current_financial_data()
        s['low'] = round(data['summaryDetail']['dayLow'], 2) or None
        s['high'] = round(data['summaryDetail']['dayHigh'], 2) or None
        s['open'] = round(data['summaryDetail']['open'], 2) or None
        s['beta'] = data['defaultKeyStatistics']['beta'] or None
        s['price'] = round(data['financialData']['currentPrice'], 2) or None
        s['prev_close'] = data['summaryDetail']['previousClose'] or None
        s['corporate_name'] = data['price']['longName'] or None
        s['percent_change'] = round(
            (s['price'] - s['prev_close']) * 100 / s['prev_close'], 2) or None

        s['volume'] = f"{int(data['summaryDetail']['volume']):,}" or None
        s['avg_volume'] = f"{data['summaryDetail']['averageVolume']:,}" or None
        s['pe_ratio'] = round(data['summaryDetail']['trailingPE'], 2) or None
        s['beta'] = round(data['defaultKeyStatistics']['beta'], 2) or None
    except:
        pass
    with lock:
        wl_data.append(s)


def _collect_graph_data(
    stock: Stock,
    return_data: list,
    lock: threading.Lock) -> None:
    """
    Queries the historical stock price data from yahoo finance.
    Appends the data to the given list. A threading lock is required
    for the data to be appended to the list.

    param:
        stock: The stock object that is to be added to the 
        to the list. The stock must have already been
        committed to the db requiring an assigned id.
        
        return_data: The list to assign the stock graph data to.
        
        lock: The treading lock to prevent writing errors to
        the return_list.
    """
    stock_data = None
    try:
        stock_data = stock.get_stock_lines(period='1y', interval='1d')
    except:
        pass
    with lock:
        return_data.append(stock_data)