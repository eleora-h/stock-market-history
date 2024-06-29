import requests
import logging
from retry import retry

# https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to

class Polygon():
    def __init__(self):
        self.auth_token = self.__get_authentication_key()
        self.__configure_logger()
        self.tickers = {}

    def __get_authentication_key(self):
        reader = open('credentials')
        reader = reader.read()
        key = reader.split(":")[1].strip()
        return key

    def __configure_logger(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s', 
            level=logging.INFO, 
            datefmt='%m-%d-%Y %I:%M:%S%p'
        )

    def get_tickers(self):
        if not self.tickers:
            self.__set_tickers()
        print('\nList of available tickers:')
        for t in self.tickers:
            print(t)

    def get_ticker_info(self, ticker):
        ticker_upper = ticker.upper()
        if ticker_upper in self.tickers:
            print(self.tickers[ticker_upper])
        else:
            print('Ticker not found. Please make sure you are providing the ticker shorthand.')

    @retry(RuntimeError, tries=3, delay=30)
    # didn't add support for pagination because this is a demo and rate limited on API as a free user
    def __set_tickers(self):
        logging.debug('entering ticker call')
        url = "https://api.polygon.io/v3/reference/tickers?active=true&limit=100&apiKey={0}".format(self.auth_token)
        response = requests.get(url)
        if response.status_code == 200:
            logging.debug('Tickers pulled successfully.')
            self.__parse_tickers(response.json())
        else:
            logging.info('Timing out on connecting to API in polygon get_tickers call. Retrying...')
            raise RuntimeError()

    def __parse_tickers(self, dict):
        try:
            for t in dict.get('results'):
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