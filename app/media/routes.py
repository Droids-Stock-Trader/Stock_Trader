from flask import current_app, render_template, abort, flash
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
    # calls the news api based on the given corporate names
    if len(stock_names) > 0:
        status_code, articles, message = News.search_news_results(stock_names, 1)
    # if the user has an empty portfolio, the user is presented
    # with the latest finantial, business, and economic news.
    else:
        status_code, articles, message = News.latest_headlines(1)
    # if there was an error, redirect to 500 internal error page.
    if status_code != 200:
        flash(message)
        abort(500)
    return render_template(
        "media/headlines.html",
        title="News Headlines",
        articles=articles,
        status_code=status_code,
        message=message,
    )
