import datetime
from io import StringIO

import pandas
import pytz
import requests

import Constants


def generate_current_timestamp():
    today = datetime.datetime.today().timetuple()
    timezone = pytz.timezone("GMT")
    return int(datetime.datetime(today[0], today[1], today[2], 0, 0, tzinfo=timezone).timestamp())


def call_service(coin, currency):
    url = construct_url(coin, currency)
    response = requests.get(url)

    if response.status_code != Constants.SUCCESS_RESPONSE_CODE:
        print("web service call failed with error code: ", response.status_code)
        raise Exception("ApiError")
    else:
        return response.content


def construct_url(coin, currency):
    current_timestamp = generate_current_timestamp()
    url = Constants.BASE_URL + Constants.CRYPTO_DICT.get(coin) + "-" + Constants.CURRENCY_DICT.get(currency)
    url += "?period1=1568764800&period2=" + str(current_timestamp)
    url += "&interval=" + Constants.INTERVAL_DAY + "&events=" + Constants.EVENTS_HISTORY + "&includeAdjustedClose=" + str(Constants.ADJUSTED_CLOSE_TRUE).lower()
    print("framed url: ", url)

    return url


def load_stock_data(coin, currency):
    stock_data = call_service(coin, currency)
    return pandas.read_csv(StringIO(str(stock_data, 'utf-8')))
