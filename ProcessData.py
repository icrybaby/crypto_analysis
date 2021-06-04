import datetime
import os
import statistics

import numpy
import pandas

import Constants
import LoadData
from tqdm.autonotebook import tqdm

import Util

tqdm.pandas()
stock_data = pandas.DataFrame()


class ProcessData:
    total_records = 0
    cleaned_records = 0
    today = str(datetime.datetime.today())

    def __init__(self, crypto, currency, moving_average_period):
        self.crypto = crypto
        self.currency = currency
        self.moving_average_period = moving_average_period
        self.stage = ""

    def get_data(self):
        today = str(datetime.datetime.today())
        print("-----" + today + "-----")
        # current_dir = os.path.dirname(os.path.realpath(__file__))

        filename = Util.generate_filename(self.crypto, self.currency, self.stage)
        if os.path.exists(Constants.DATASET_DIRECTORY + "/" + filename):
            return pandas.read_csv(Constants.DATASET_DIRECTORY + "/" + filename)
        else:
            dataframe = LoadData.load_stock_data(self.crypto, self.currency)
            Util.save_data(dataframe, "raw")
            return dataframe

    def clean_data(self, dataframe):
        columns = dataframe.columns
        print("Dataframe dimension: ", dataframe.info())
        print("Columns: ", columns)
        self.total_records = len(dataframe)
        print("Total records before cleaning: ", self.total_records)

        dataframe.dropna(axis=0, inplace=True, how='any')
        self.cleaned_records = len(dataframe)
        print("Total non-empty records: ", self.cleaned_records)
        print("Data lost: ", (self.total_records - self.cleaned_records) / self.total_records)
        dataframe.Date = pandas.to_datetime(dataframe.Date)

        return dataframe

    def add_synthetic_data(self, dataframe):
        dataframe['syn_day_difference'] = dataframe['Open'] - dataframe['Adj Close']
        dataframe['syn_day_variation'] = dataframe['High'] - dataframe['Low']
        dataframe = self.calculate_moving_average(dataframe)
        # dataframe['syn_simple_moving_average'] = numpy.convolve(dataframe.loc[:, 'Close'],
        # numpy.ones(self.moving_average_period), 'same') / self.moving_average_period
        dataframe['syn_exponential_moving_average'] = dataframe.loc[:, 'Adj Close'].ewm(span=15, adjust=False).mean()
        dataframe['syn_volatility'] = numpy.log(dataframe['Adj Close'].shift(1) / dataframe['Adj Close']) * 100

        Util.save_data(dataframe, Constants.STAGE_PROCESSED)

    def calculate_moving_average(self, dataframe):
        total_days = len(dataframe)

        for ma in self.moving_average_period:
            moving_average = []
            for end_index in reversed(range(total_days)):
                start_index = end_index - ma

                if start_index >= 0:
                    moving_average.append(statistics.mean(dataframe.loc[start_index:end_index, 'Adj Close']))
                else:
                    moving_average.append(statistics.mean(dataframe.loc[0:4, 'Adj Close']))
            moving_average.reverse()
            dataframe['syn_sma_' + str(ma)] = moving_average

        return dataframe

