import datetime
import os

import AnalyzeData
import Constants

today = str(datetime.datetime.today())


def file_clean(self):
    try:
        if not os.path.exists(Constants.DATASET_DIRECTORY):
            os.mkdir(Constants.DATASET_DIRECTORY)
        else:
            for file in os.listdir(Constants.DATASET_DIRECTORY):
                if self.today.split()[0] not in file:
                    os.remove(os.path.join(Constants.DATASET_DIRECTORY, file))
    except OSError:
        print("exception during initial directory setup / file cleaning")


def save_data(dataframe, stage):
    filename = generate_filename(stage)
    filename = Constants.DATASET_DIRECTORY + "/" + filename

    if os.path.exists(filename):
        os.remove(filename)

    dataframe.to_csv(filename, index=False)


def generate_filename(crypto, currency, stage):
    filename = crypto + "-" + currency + "-" + today.split()[0] + "-" + stage + ".csv"

    return filename


def generate_push_message():
    pass
