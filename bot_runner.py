# import sys, os
# sys.path.append(os.path.abspath(os.getcwd()))

import plotly.express as px
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os, time

from accounts.mt5_account import Login, Get_Balance, Get_Orders
from calculators.lot_size import Lot_Calc
from calculators.pip_size import Pip_Calc
from calculators.take_profit import TakeProfit_Calc
from calculators.stop_loss import StopLoss_Calc
from discord_utils.webhook import Send_Log
from fetch_data.mt5_data import Data_Candles
from order_utils.mt5_order import Place_Order, Close_Order
from trading_strategies.bollinger import Bollinger_Calc
from trading_strategies.rsi import RSI_Calc
from trading_strategies.sma import SMA_Calc
from trading_strategies.ema import EMA_Calc
from trading_strategies.atr import ATR_Calc

# Load file .env
from dotenv import load_dotenv
load_dotenv()

# .env information
mt5_account = int(os.getenv('MT5_ACCOUNT'))
mt5_password = str(os.getenv('MT5_PASSWORD'))
mt5_server = str(os.getenv('MT5_SERVER'))

# URL webhook for log message
webhook_fx = os.getenv('DISCORD_WEBHOOK_FX')

def main():
    # Initialize MetaTrader 5 and login
    mt5.initialize()
    if not Login(mt5_account, mt5_password, mt5_server):
        Send_Log(webhook_fx, "Login failed.")
        return

    # Get account balance
    account_balance = Get_Balance()

    # Pair information
    symbol = 'BTCUSD'
    pip_size = Pip_Calc(symbol)

    # Calculate lot with risk percentage
    lot_size = Lot_Calc(account_balance, 1, 2016, pip_size)
    print(lot_size)

    # Timeframe
    timeframe = mt5.TIMEFRAME_M1

    while True:
        # Fetch the latest candlestick data
        data = Data_Candles(symbol, timeframe, 1000)


        df = Bollinger_Calc(data)
        
        df['RSI'] = RSI_Calc(data)
        print(df)
        return
        df['SMA'] = SMA_Calc(data)
        df['EMA'] = EMA_Calc(data)
        df['ATR'] = ATR_Calc(data)

        print(df)
        return
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        atr = last_row['ATR']
        upper_band = last_row['upper_band']
        lower_band = last_row['lower_band']

        # Buy condition
        if (prev_row['EMA'] < prev_row['SMA'] and last_row['EMA'] > last_row['SMA'] and
            last_row['RSI'] < 30 and last_row['close'] <= lower_band):
            stop_loss = StopLoss_Calc(last_row['close'], 'buy', atr, lower_band)
            take_profit = TakeProfit_Calc(last_row['close'], 'buy', atr)

            if Place_Order(symbol, 'buy', lot_size, stop_loss, take_profit):
                Send_Log(webhook_fx, f"Buy order placed for {symbol} at {last_row['close']}, SL: {stop_loss}, TP: {take_profit}")

        # Sell condition
        elif (prev_row['EMA'] > prev_row['SMA'] and last_row['EMA'] < last_row['SMA'] and
            last_row['RSI'] > 70 and last_row['close'] >= upper_band):
            stop_loss = StopLoss_Calc(last_row['close'], 'sell', atr, upper_band)
            take_profit = TakeProfit_Calc(last_row['close'], 'sell', atr)

            if Place_Order(symbol, 'sell', lot_size, stop_loss, take_profit):
                Send_Log(webhook_fx, f"Sell order placed for {symbol} at {last_row['close']}, SL: {stop_loss}, TP: {take_profit}")

if __name__ == "__main__":
    main()
   
