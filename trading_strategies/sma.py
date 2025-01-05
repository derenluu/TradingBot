import sys, os
sys.path.append(os.path.abspath(os.getcwd()))

import MetaTrader5 as mt5
import pandas as pd
import numpy as np

from fetch_data.mt5_data import Data_Candles

def SMA_Calc(symbol, timeframe, fast_sma, slow_sma):
    mt5.initialize()
    data = Data_Candles(symbol, timeframe, 1000)

    data_slow_sma = data['close'].rolling(slow_sma).mean();
    print(data_slow_sma)
    return data_slow_sma

    # return data[column].rolling(window=period).mean()

SMA_Calc('BTCUSD', mt5.TIMEFRAME_M1, 10, 100)