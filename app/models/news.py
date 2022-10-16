from requests import request
from datetime import datetime as dt
from app import db
from flask import current_app

class News(db.Model):
    __tablename__ = 'news'

    ID_LENGTH = 32
    CLEAN_URL_LENGTH = 128
    TITLE_LENGTH = 512
    AUTHOR_LENGTH = 128
    EXCERPT_LENGTH = 1024
    URL_LENGTH = 2046

    id = db.Column(db.String(ID_LENGTH), primary_key=True)
    title = db.Column(db.String(TITLE_LENGTH))
    author = db.Column(db.String(AUTHOR_LENGTH))
    published_date = db.Column(db.DateTime)
    link = db.Column(db.String(URL_LENGTH))
    clean_url = db.Column(db.String(CLEAN_URL_LENGTH))
    excerpt = db.Column(db.String(EXCERPT_LENGTH))
    media = db.Column(db.String(URL_LENGTH))

    def search_news_results(query, page) -> list:
        formatted_query = ' OR '.join(['"' + name + '"' for name in query])
        params = {
            'q': formatted_query,
            'countries': 'US',
            'lang': 'en',
            'sort_by': 'date',
            'page_size': current_app.config['HEADLINES_ARTICLE_CNT'],
            'to_rank': 10000,
            'page': page
        }
        headers = {'x-api-key': current_app.config['NEWSCATCHER_API_KEY']}
        response = request('GET', current_app.config['NEWSCATCHER_API_URL'],
                            headers=headers, params=params)
        status_code = response.status_code

        if status_code == 200:
            articles = response.json()['articles']
            for i in range(len(articles)):
                articles[i]['published_date'] = dt.strptime(
                    articles[i]['published_date'], '%Y-%m-%d %H:%M:%S')
            message = 'Success'
        else:
            articles = []
            message = response.json()['message']

        return [status_code, articles, message]
    