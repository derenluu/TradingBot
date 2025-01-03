import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os
import time

from dotenv import load_dotenv
from account.account import Login, Logout, Get_Balance, Get_Trades
from calculate.lot_size import Calculator_Lot
from discord.webhook import send_log

# Load biến môi trường từ file .env
load_dotenv()

def main():
    account = int(os.getenv("MT5_ACCOUNT"))
    password = os.getenv("MT5_PASSWORD")
    server = os.getenv("MT5_SERVER")
    webhook_fx = os.getenv("DISCORD_WEBHOOK_FX")

    while True:
        send_log(webhook_fx, account)
        time.sleep(2)   # Limit webhook 2 second (30 request per minute)
        print("Log sent:", account)


    # Đăng nhập vào MetaTrader 5
    # if not Login(account, password, server):
    #     send_log(webhook_url, "Login thất bại.")
    #     return

    # Lấy số dư tài khoản
    # balance = Get_Balance()

    # if balance is not None:
    #     send_log(webhook_url, f"Login thành công! Số dư hiện tại: {balance}")
    #     print(f"Current balance: {balance}")
    # else:
    #     send_log(webhook_url, "Login thành công nhưng không lấy được số dư tài khoản.")
    #     print("Could not retrieve balance.")

    # Đóng kết nối với MT5
    # mt5.shutdown()

if __name__ == "__main__":
    main()
