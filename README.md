# Stock Trader

## Setup

Make sure that you have at least python 3.8 installed. Steps 1, 2, 4, and 5 only need to be performed once (step 5 needs to be performed every time we modify the database). 

1. Clone the repository

    ```
    $ git clone git@github.com:tmsoc/Stock_Trader.git
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
5. build the database.
    ```
    (venv) $ flask db upgrade
    ```
6. Activate the web server.
    ```
    (venv) $ flask run
    ```
    At this point the web app can be reached at `localhost:5000`. To terminate the web server, just enter `Ctrl + C` into your terminal.

