import os.path

import Constants

from multiprocessing import Pool
import yfinance as yf
import pandas
import time

stocks = ['tcs', 'infy']
market = 'NS' # nse
symbols = []
for stock in stocks:
    symbols.append(stock + "." + market)


def retrieve_live_data(symbol):
    filename = Constants.LIVE_DATASET_DIRECTORY + "/" + symbol + Constants.FILE_EXTENSION
    if os.path.exists(Constants.LIVE_DATASET_DIRECTORY):
        if os.path.exists(filename):
            os.remove(filename)
    else:
        os.mkdir(Constants.LIVE_DATASET_DIRECTORY)

    df = yf.Ticker(symbol).history(period='1d', interval='15m')
    df.to_csv(filename)


while True:
    with Pool(os.cpu_count()) as pool:
        pool.map(retrieve_live_data, symbols)
        time.sleep(900)  # sleep for 15 minutes













