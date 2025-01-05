import plotly.express as px
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os
import time

from accounts.mt5_account import Login, Get_Balance, Get_Orders
from calculators.lot_size import Lot_Calc
from calculators.pip_size import Pip_Calc
from discord_utils.webhook import send_log
from order_utils.mt5_order import Place_Order, Close_Order
# from trading_strategies.ma import ma_strategy

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
        send_log(webhook_fx, "Login failed.")
        return

    # Get account balance
    account_balance = Get_Balance()

    # Pair information
    symbol = 'BTCUSD'
    pip_size = Pip_Calc(symbol)

    # Timeframe
    timeframe = mt5.TIMEFRAME_M1

    # while True:
        # Fetch the latest candlestick data
        # data = get_candlestick_data(symbol, timeframe, 100)
        # if data is None:
        #     send_log(webhook_fx, f"Failed to get candlestick data for {symbol}.")
        #     continue

    # Calculate lot with risk percentage
    # lot_size = Lot_Calc(account_balance, 1, 2016, pip_size)
    # print(lot_size)


    # print(f"Pip size: {pip_size}")
    # if account_balance is None:
    #     send_log(webhook_fx, "Failed to retrieve account balance.")
    #     return
    
    # send_log(webhook_fx, f"Login successful! Current balance: {account_balance}")
    # order_ticket = Place_Order(symbol, 'buy', 0.05, 0.0, 0.0)
    # time.sleep(5)
    # Close_Order(order_ticket)

if __name__ == "__main__":
    main()
   
