from flask import current_app, render_template, abort, flash, request
from flask_login import current_user, login_required
from app import db
from app.media import bp
from app.models import News


@bp.route("/headlines")
@login_required
def headlines():
    # gets the corporate names of all the stocks within
    # the current users portfolio in list form
    stock_names = current_user.portfolio_corporate_names
    # gets the current news page from the url
    # if no page is given, default is 1
    page = request.args.get('page', 1, int)
    # calls the news api based on the given corporate names
    if len(stock_names) > 0:
        results = News.search_news_results(stock_names, page)
    # if the user has an empty portfolio, the user is presented
    # with the latest finantial, business, and economic news.
    else:
        results = News.latest_headlines(page)
    # if there was an error, redirect to 500 internal error page.
    if results['status_code'] != 200:
        flash(results['message'])
        abort(500)
    return render_template(
        "media/headlines.html",
        title="News Headlines",
        articles=results['articles'],
        status_code=results['status_code'],
        message=results['message'],
        prev_url=results['prev_url'],
        next_url=results['next_url']
    )
