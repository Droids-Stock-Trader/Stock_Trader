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
def stock():
    """ Stock Info Route """
    # If user is logged in here, nothing to do, return to index.
    if current_user.is_authenticated:
        symbol = request.args.get('stock')
        asset = Stock.get_stock_info(symbol).dict()
        print(asset)
        return render_template('stock/stock.html', title=f'{symbol} Details', stock=asset)
    return redirect(url_for('main.welcome'))

@bp.route('/stock_info', methods=['POST'])
@login_required
def stock_info():
    """ Endpoint for processing stock info requests """
    symbol = request.form['symbol']
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    return Stock.get_stock_bars(symbol, TimeFrame.Hour, yesterday)