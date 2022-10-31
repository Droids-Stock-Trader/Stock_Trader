from flask import render_template, url_for, current_app, request
from flask_login import current_user, login_required
from app import db
from app.history import bp
from app.models import History


@bp.route('/account_history')
@login_required
def account_history():
    """
    Renders account history page.
    """
    # gets the next page for pagination
    page = request.args.get('page', 1, type=int)
    # queries the current page of history records
    # records are sorted by date in decending order
    history = History.query.filter_by(
        user_id=current_user.id).order_by(
            History.timedata.desc()).paginate(
                page=page, 
                per_page=current_app.config['HISTORY_LISTING_CNT'],
                error_out=False)
    # previous/next url for the pagination links
    prev_url = url_for('history.account_history', page=history.prev_num) \
        if history.has_prev else None
    next_url = url_for('history.account_history', page=history.next_num) \
        if history.has_next else None

    return render_template(
        'history/account_history.html', 
        title='Account History', history=history.items,
        prev_url=prev_url, next_url=next_url)