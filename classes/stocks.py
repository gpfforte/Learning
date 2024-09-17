import datetime as dt

import numpy as np
import pandas as pd

# import pandas_datareader as pdr
# import pandas_datareader.data as web
import yfinance as yf

# aapl = pdr.get_data_yahoo(
#     "AAPL", start=datetime.datetime(2006, 10, 1), end=datetime.datetime(2012, 1, 1)
# )
# df = pdr.get_data_fred("GS10")
# print(df)
# df = web.DataReader("GE", "yahoo", start="2019-09-10", end="2019-10-09")
# aapl = web.DataReader(
#     "aapl",
#     "yahoo",
#     # start="2019-09-10",
#     # end="2019-10-09"
#     start=datetime.datetime(2022, 10, 1),
#     end=datetime.datetime(2023, 12, 1),
# )
now = dt.datetime.now()
scarica = False
if scarica:
    aapl = yf.download(
        "aapl",
        # start="2019-09-10",
        # end="2019-10-09"
        start=dt.datetime(2022, 10, 1),
        end=now,
    )
    print(aapl)

    msft = yf.download(
        "msft",
        # start="2019-09-10",
        # end="2019-10-09"
        start=dt.datetime(2022, 10, 1),
        end=now,
    )
    print(msft)


class Stock:
    def __init__(self, symbol, *args):
        self.symbol = symbol
        self.ticker = yf.Ticker(self.symbol)
        self.info = self.ticker.get_info()
        if args:
            if args[0] is not None:
                self.bars = args[0]
            if args[1] is not None:
                self.short_window = args[1]
            if args[2] is not None:
                self.long_window = args[2]

    def print_info(self):
        for key in self.info:
            print(key, self.info[key])

    def get_values(self, start, end):
        self.bars = yf.download(self.symbol, start, end)

    def moving_average_set_parameters(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        signals = pd.DataFrame(index=self.bars.index)
        signals["signal"] = 0.0

        signals["short_mavg"] = (
            self.bars["Close"]
            .rolling(window=self.short_window, min_periods=1, center=False)
            .mean()
        )
        signals["long_mavg"] = (
            self.bars["Close"]
            .rolling(window=self.long_window, min_periods=1, center=False)
            .mean()
        )

        signals["signal"][self.short_window :] = np.where(
            signals["short_mavg"][self.short_window :]
            > signals["long_mavg"][self.short_window :],
            1.0,
            0.0,
        )

        signals["positions"] = signals["signal"].diff()

        return signals


if scarica:
    apple = Stock("aapl", aapl, 40, 100)
    print(apple.generate_signals())
    microsoft = Stock("msft", msft, 40, 100)
    print(microsoft.generate_signals())

ucg = Stock("UCG.MI")
ucg.get_values(
    start=dt.datetime(2022, 10, 1),
    end=now,
)
ucg.moving_average_set_parameters(40, 100)
print(ucg.generate_signals())
if scarica:
    ucg.print_info()
    apple.print_info()
    microsoft.print_info()

