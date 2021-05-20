import datetime
from io import StringIO

import pandas
import pytz
import requests

BASE_URL = "https://query1.finance.yahoo.com/v7/finance/download/"
interval = '1d'  # day's chart
events = 'history'
adjusted_close = True

crypto = {"doge": "DOGE-INR"}


def generate_current_timestamp():
    today = datetime.datetime.today().timetuple()
    timezone = pytz.timezone("GMT")
    return int(datetime.datetime(today[0], today[1], today[2], 0, 0, tzinfo=timezone).timestamp())


def call_service(type):
    url = construct_url(type)
    response = requests.get(url)

    if response.status_code != 200:
        print("web service call failed with error code: ", response.status_code)
        raise Exception("ApiError")
    else:
        return response.content


def construct_url(type):
    current_timestamp = generate_current_timestamp()
    url = BASE_URL + crypto.get(type)
    url += "?period1=1568764800&period2=" + str(current_timestamp)
    url += "&interval=" + interval + "&events=" + events + "&includeAdjustedClose=" + str(adjusted_close).lower()
    print("framed url: ", url)

    return url


def load_stock_data(type):
    stock_data = call_service(type)
    return pandas.read_csv(StringIO(str(stock_data, 'utf-8')))
