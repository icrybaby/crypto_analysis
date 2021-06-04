import Constants
import Util
from ProcessData import ProcessData

cryptos = ["doge"]
currency = "inr"
moving_average = Constants.ALL_MOVING_AVERAGES

Util.file_clean()

def get_historical_data():
    for crypto in cryptos:
        process = ProcessData(crypto, currency, moving_average)
        dataset = process.get_data()
        process.add_synthetic_data(process.clean_data(dataset))


def analyze_data():




get_historical_data()