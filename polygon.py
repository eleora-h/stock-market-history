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
        key = reader.split(":")[1]
        return key

    def __configure_logger(self):
        pass

    def __send_request(self):
        pass

    def run(self):
        self.__get_authentication_key()