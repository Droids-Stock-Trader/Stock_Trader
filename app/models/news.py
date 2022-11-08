from requests import request
from datetime import datetime as dt
from app import db
from flask import current_app
from flask_login import current_user


class News(db.Model):
    __tablename__ = "news"

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

    @staticmethod
    def search_news_results(query: list, page: int) -> dict:
        """
        Calls the news api quering news articles that are
        related the to list of key phases provide. Returns
        a dictionary contining the status code, articles, api message,
        and next/previous pages.

        Params
        ------
        query - A List of key phases to search for.
        page - The current page of headlines to return
        """
        formatted_query = " OR ".join(['"' + name + '"' for name in query])
        url = current_app.config["NEWSCATCHER_API_URL"]
        params = {
            "q": formatted_query,
            "countries": "US",
            "lang": "en",
            "topic": current_user.news_settings.topics,
            "sort_by": "date",
            "page_size": current_app.config["HEADLINES_ARTICLE_CNT"],
            "to_rank": 10000,
            "page": page,
        }
        headers = {"x-api-key": current_app.config["NEWSCATCHER_API_KEY"]}
        return News._call_news_api(url, params, headers)

    @staticmethod
    def latest_headlines(page: int) -> dict:
        """
        Returns the latest headlines that are related
        to either finance, business, or economics. Returns
        a dictionary contining the status code, articles, 
        api message, and next/previous pages.

        Params
        ------
        page - The current page of headlines to return 
        """
        url = current_app.config["NEWSCATCHER_API_GEN_URL"]
        params = {
            "countries": "US",
            "lang": "en",
            "topic": current_user.news_settings.topics,
            "page_size": current_app.config["HEADLINES_ARTICLE_CNT"],
            "page": page,
        }
        headers = {"x-api-key": current_app.config["NEWSCATCHER_API_KEY"]}
        return News._call_news_api(url, params, headers)

    @staticmethod
    def _call_news_api(url: str, params: dict, headers: dict) -> dict:
        """
        Performs the api call to the given url and Returns
        a dictionary contining the status code, articles, api message,
        and next/previous pages.

        Params
        ------
        url - URL for the new Request object.
        params - Dictionary, list of tuples or bytes to send
                 in the query string for the Request.
        headers - Dictionary of HTTP Headers to send with the Request.
        """
        # performs the api call and extracts the returned status code.
        response = request("GET", url=url, headers=headers, params=params)
        status_code = response.status_code
        # If the call was successful, extract the acticles from the response
        # into a list, parses the published dates into python datatime objects
        # and calculates the next/previous pagination numbers.
        response_dict = response.json()
        if status_code == 200 and int(response_dict['total_hits']) > 0:
            articles = response_dict["articles"]
            for i in range(len(articles)):
                articles[i]["published_date"] = dt.strptime(
                    articles[i]["published_date"], "%Y-%m-%d %H:%M:%S"
                )
            message = None
            # Pagination
            current_page = int(params['page'])
            total_pages = response_dict['total_pages']
            prev_url = current_page - 1 if current_page > 1 else None
            next_url = current_page + 1 if current_page < total_pages else None
        # if the response has an error, return an empty list along
        # with the error message.
        elif int(response_dict['total_hits']) == 0:
            articles = []
            message = 'No relavent articles found. Try broadening your settings news topics'
            prev_url = None
            next_url = None
        else:
            articles = []
            message = response_dict["message"]
            prev_url = None
            next_url = None

        return {'status_code': status_code,
                'articles': articles,
                'message': message,
                'prev_url': prev_url,
                'next_url': next_url}
