from flask import render_template, url_for, redirect
from flask_login import current_user, login_required
from app import db
from app.history import bp


@bp.route('/account_history')
@login_required
def account_history():
    """
    Renders account history page.
    """
    history = current_user.history_list
    return render_template(
        'history/account_history.html', 
        title='Account History', history=history)
