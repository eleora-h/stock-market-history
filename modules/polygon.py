import requests
import logging
import modules.graphs as graphs
from retry import retry

# https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to

class Polygon():
    def __init__(self):
        self.auth_token = self.__get_authentication_key()
        self.__configure_logger()
        self.tickers = {}
        self.__set_tickers()

    def __configure_logger(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s', 
            level=logging.INFO, 
            datefmt='%m-%d-%Y %I:%M:%S%p'
        )

    def __get_authentication_key(self):
        reader = open('credentials')
        reader = reader.read()
        key = reader.split(":")[1].strip()
        return key
    
    def get_tickers(self):
        print('\nList of available tickers:')
        for t in self.tickers:
            print(t)

    def get_ticker_info(self, ticker):
        ticker_upper = ticker.upper()
        if ticker_upper in self.tickers:
            print(self.tickers[ticker_upper])
        else:
            print('Ticker not found. Please make sure you are providing the ticker shorthand.')

    # Default wrapper method for calling the Polygon API. No pagination support because demo and rate limited on API as a free user.
    @retry(RuntimeError, tries=3, delay=120)
    def __send_polygon_request(self, url):
        logging.info('Entering Polygon API request call.')
        response = requests.get(url)
        if response.status_code == 200:
            logging.info('Response successful.')
            return response.json()
        else:
            logging.info('Timing out on connecting to API in polygon get_tickers call. Retrying in 120 seconds.')
            raise RuntimeError("Timed out, retrying in 120 seconds.")

    def __set_tickers(self):
        url = "https://api.polygon.io/v3/reference/tickers?active=true&limit=100&apiKey={0}".format(self.auth_token)
        response = self.__send_polygon_request(url)
        try:
            for t in response.get('results'):
                shorthand = t['ticker']
                info = {
                    'name': t['name'],
                    'type': t['market'],
                    'currency_name': t['currency_name'],
                    'last_update': t['last_updated_utc']
                }
                self.tickers[shorthand] = info
        except Exception as e:
            raise Exception('Unexpected error while parsing ticker data. Terminating program. Error: ' + str(e))
        
    def get_news(self, ticker):
        url = "https://api.polygon.io/v2/reference/news?limit=3&ticker={0}&apiKey={1}".format(ticker, self.auth_token)
        response = self.__send_polygon_request(url)
        if response.get('results'):
            print('Success!')
        else:
            print('No results found :(.\nRetrying for all tickers to demo feature.')
            url = "https://api.polygon.io/v2/reference/news?limit=3&apiKey={0}".format(self.auth_token)
            response = self.__send_polygon_request(url)
            if not response.get('results'):
                raise RuntimeError('No news results could be found at time, suspected error lies with API. Please try program again later.')
        title = """
        -----------------
        NEWS RESULTS
        -----------------
        """
        print(title)
        try:
            for n in response.get('results'):
                n_string = """
                TITLE: {0}
                AUTHOR: {1}
                URL: {2}
                DATE: {3}
                """.format(n['title'], n['author'], n['article_url'], n['published_utc'])
                print(n_string)
        except Exception as e:
            raise Exception('Unexpected error while parsing news data. Terminating program. Error: ' + str(e))

    def get_dividends(self, ticker):
        url = "https://api.polygon.io/v3/reference/dividends?ticker={0}&limit=10&apiKey={1}".format(ticker, self.auth_token)
        response = self.__send_polygon_request(url)
        try:
            x_axis = []
            y_axis = []
            title = """
        -----------------
        DIVIDENDS for {0}
        Returned in date: $ (dividend type)
        -----------------
            """.format(ticker)
            print(title)
            if not response.get('results'):
                print('No results found for {0}. Try -d "ABBV" for a demo.'.format(ticker))
            else:
                for d in response.get('results'):
                    d_string = '{0}: ${1} ({2})'.format(d['pay_date'], d['cash_amount'], d['dividend_type'])
                    print(d_string)
                    x_axis.append(d['pay_date'])
                    y_axis.append(d['cash_amount'])
                graphs.graph(x_axis, y_axis, 'Dividends for {0} over Time (USD $)'.format(ticker), 'Date', 'Cash Amount (%)')
        except Exception as e:
            raise Exception('Unexpected error while parsing dividend data. Terminating program. Error: ' + str(e))