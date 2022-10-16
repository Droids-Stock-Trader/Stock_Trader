from flask import render_template, url_for, redirect
from flask_login import current_user, login_required
from app import db
from app.media import bp
from app.models import News
from datetime import datetime as dt

# development data
from app.models._development_data import dev_articles

@bp.route('/headlines')
@login_required
def headlines():
    stock_names = current_user.portfolio_corporate_names
    status_code, articles, message = News.search_news_results(stock_names, 1)
    print(status_code)
    print(message)
    # This code segment is temporary and will be replace in TD-52.
    # In TD-52 I'll add the proper validations and condition handeling.
    # I'm adding it for the sprint retrospective for when we demo.
    # ===========================================================
    # articles = dev_articles
    # if isinstance(articles[0]['published_date'], str):
    #     for i in range(len(articles)):
    #         date_str = articles[i]['published_date']
    #         articles[i]['published_date'] = dt.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    # ===========================================================
    return render_template('media/headlines.html', 
                           title='News Headlines', articles=articles)