import requests
import retrying
import logging

# https://polygon.io/docs/stocks/get_v2_aggs_ticker__stocksticker__range__multiplier___timespan___from___to

class Polygon():
    def __init__(self):
        self.auth_token = self.__get_authentication_key()
        self.__configure_logger()

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
        url = "https://api.polygon.io/v3/reference/tickers?active=true&limit=100&apiKey={0}".format(self.auth_token)
        response = requests.get(url)
        if response.status_code == 200:
            print('success!')
            print(response.text)
        # probably want to store as a pandas dataframe or similar for easy querying (or just dict?)

    def __send_request(self):
        pass

    def run(self):
        logging.info('STARTING SCRIPT.')
        print(self.auth_token)
        logging.info('TERMINATING SCRIPT.')