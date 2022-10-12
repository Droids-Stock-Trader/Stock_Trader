from flask import render_template, url_for, redirect
from flask_login import current_user, login_required
from app import db
from app.media import bp
from datetime import datetime as dt

# development data
from app.models._development_data import dev_articles

@bp.route('/headlines')
@login_required
def headlines():
    # This code segment is temporary and will be replace in TD-52.
    # In TD-52 I'll add the proper validations and condition handeling.
    # I'm adding it for the sprint retrospective for when we demo.
    # ===========================================================
    articles = dev_articles
    for article in articles:
        date_str = article['published_date']
        article['published_date'] = dt.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    # ===========================================================
    return render_template('media/headlines.html', 
                           title='News Headlines', articles=articles)