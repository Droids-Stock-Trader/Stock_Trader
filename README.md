# Stock Trader
Stock Trader is a web application for individuals who want an easy, real-time way to monitor the stock market and their investments. The application has the capability to provide alerts on specific stocks or companies, allows the user to make transactions, and provides links to relevant news articles to keep users up to date. The application is geared towards users who want quick, anytime, anywhere access to stock market information and the ability to easily make transactions on the go.

This software is in development as a Computer Science Senior Project for the Fall 2022 semester of CECS 491 at [California State Univerisity Long Beach](https://www.csulb.edu/). 

## Table of Contents
- [Setup](#Setup)
- [3rd Party APIs](#API)
- [Authors](#Authors)

## Setup
Make sure that you have at least python 3.8 installed. Steps 1, 2, 4, and 5 only need to be performed once (step 6 needs to be performed every time we modify the database). 

1. Clone the repository

    ```
    $ git clone https://github.com/Droids-Stock-Trader/Stock_Trader.git
    $ cd Stock_Trader
    ```

2. Setup your the vertual environment of your choosing. Since I developed this with python, I just used venv.
    ```
    $ python -m venv venv
    ```
3. Activate the environment.
    ```
    $ # for linux and mac (pretty sure this is the mac activation)
    $ source venv/bin/activate
    (venv) $
    ```
    ```
    $ # for windows (scripts need to be enabled for this to work)
    $ venv\Scripts\activate
    (venv) $
    ```
     You should now be able to see the name of your envirornment before the command prompt.
4. Install all of the dependencies. 
    ```
    (venv) $ pip install -r requirements.txt
    ```
5. Setup your environment variables. Within the same directory as the config.py file, create a file named ".env". Add the following environment variables to the file.
    ```
    SECRET_KEY=<your secret cryptographic key>
    NEWSCATCHER_API_KEY=<api key provided by https://newscatcherapi.com/>
    SENDGRID_API_KEY=<api key provided by https://sendgrid.com/>
    MAIL_DEFAULT_SENDER=<a valid PAID for email address>
    ALPACA_API_KEY=<api ID key provided by https://alpaca.markets/>
    ALPACA_SECRET_KEY=<secret key provided by https://alpaca.markets/>
    ```
6. build the database.
    ```
    (venv) $ flask db upgrade
    ```
7. Activate the web server.
    ```
    (venv) $ flask run
    ```
    At this point the web app can be reached at `localhost:5000`. To terminate the web server, just enter `Ctrl + C` into your terminal.


## API
- [Alpaca](https://alpaca.markets): Trade with algorithms, connect with apps, and build services with our easy to use APIs. https://alpaca.markets
- [Newscatcher](https://newscatcherapi.com): Search multi-language worldwide news articles published online with NewsCatcher's News API. https://newscatcherapi.com
- [Sendgrid](https://sendgrid.com): A cloud-based service that assists businesses with email delivery. https://sendgrid.com

## Authors
* **Jerry Aragon** - https://github.com/J-Kid-Beast
* **Benjamin Okenwa** - https://github.com/BenjaminGreat5
* **Jacob Pradels** - https://github.com/jacobpradels
* **Tony Samaniego** - https://github.com/tmsoc