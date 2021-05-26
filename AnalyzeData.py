import pandas

dataframe = pandas.DataFrame()


class AnalyzeData:
    def __init__(self):
        self.max_price = 0
        self.max_volume = 0
        self.max_volatility = 0
        self.current_volume = dataframe.loc[len(dataframe): 'Volume']
        self.current_price = dataframe.loc[len(dataframe): 'Adj Close']
        self.current_volatility = dataframe.loc[len(dataframe): 'syn_volatility']
        self.current_syn_sma_5 = dataframe.loc[len(dataframe): 'syn_sma_5']
        self.current_syn_sma_10 = dataframe.loc[len(dataframe): 'syn_sma_10']
        self.current_syn_sma_20 = dataframe.loc[len(dataframe): 'syn_sma_20']
        self.current_syn_sma_50 = dataframe.loc[len(dataframe): 'syn_sma_50']
        self.current_syn_sma_100 = dataframe.loc[len(dataframe): 'syn_sma_100']
        self.current_syn_sma_200 = dataframe.loc[len(dataframe): 'syn_sma_200']

    def analyze_volume(self):
        max_row = dataframe[dataframe['Volume'] == dataframe['Volume'].max(skipna=True)]
        self.max_volume = max_row['Adj Close']
        # print("all time high volume: ", self.max_volume/1000000, "M on ", max_row['Date'])

        if self.current_volume > self.max_volume:
            print("current volume: ", self.current_price / 1000000, "M crossed all time high volume of: ",
                  self.max_volume)

    def analyze_moving_average(self):
        if self.current_price > self.current_syn_sma_5:
            print("current price: ", self.current_price, "crossed  5 days sma: ", self.current_syn_sma_5)
        if self.current_price > self.current_syn_sma_10:
            print("current price: ", self.current_price, "crossed  10 days sma: ", self.current_syn_sma_10)
        if self.current_price > self.current_syn_sma_20:
            print("current price: ", self.current_price, "crossed  20 days sma: ", self.current_syn_sma_20)
        if self.current_price > self.current_syn_sma_50:
            print("current price: ", self.current_price, "crossed  50 days sma: ", self.current_syn_sma_50)
        if self.current_price > self.current_syn_sma_100:
            print("current price: ", self.current_price, "crossed  100 days sma: ", self.current_syn_sma_100)
        if self.current_price > self.current_syn_sma_200:
            print("current price: ", self.current_price, "crossed  200 days sma: ", self.current_syn_sma_200)

    def analyze_volatility(self):
        max_row = dataframe[dataframe['syn_volatility'] == dataframe['syn_volatility'].max(skipna=True)]
        self.max_volatility = max_row['syn_volatility']
        # print("all time high volume: ", abs(self.current_volatility), " on ", max_row['Date'])

        if abs(self.current_volatility) > abs(self.max_volume):
            print("current volatility: ", abs(self.current_volatility), " crossed all time high volatility of: ",
                  abs(self.max_volume))

    def analyze_time_high(self):
        max_row = dataframe[dataframe['Adj Close'] == dataframe['Adj Close'].max(skipna=True)]
        self.max_price = max_row['Adj Close']
        # print("all time high price: ", self.max_price, "on ", max_row['Date'])

        if self.current_price > self.max_price:
            print("current price: ", self.current_price, "crossed all time high price: ", self.max_price)
