import datetime
import os
import pandas
import LoadData

stock_data = pandas.DataFrame()


class ProcessData:
    total_records = 0
    cleaned_records = 0

    def __init__(self):
        pass

    def get_data(self):
        today = str(datetime.datetime.today())
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        filename = 'doge-' + today.split()[0] + '.csv'

        if os.path.exists('saved_dataset/' + filename):
            return pandas.read_csv('saved_dataset/' + filename)

        else:
            dataframe = LoadData.load_stock_data("doge")
            dataframe.to_csv('saved_dataset/' + filename, index=False)
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

        return dataframe


process = ProcessData()
dataset = process.get_data()
dataset = process.add_synthetic_data(process.clean_data(dataset))





