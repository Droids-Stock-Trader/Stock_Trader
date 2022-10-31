from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
from app import db
from app.stock import bp
import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv
# from app.stock.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm

@bp.route('/detail', methods=['GET', 'POST'])
def stock():
    """ Stock Info Route """
    # If user is logged in here, nothing to do, return to index.
    if current_user.is_authenticated:
        stock_name = request.args.get('stock')
        BASE_URL = "https://paper-api.alpaca.markets"
        ALPACA_API_KEY = os.environ.get('ALPACA_API_KEY')
        ALPACA_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY')
        api = tradeapi.REST(key_id=ALPACA_API_KEY, secret_key=ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')
        stock_data = api.get_asset(stock_name)
        return render_template('stock/stock.html', title=f'{stock_data.symbol} Details', stock=stock_data)
    return redirect(url_for('main.index'))
