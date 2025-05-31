import MetaTrader5 as mt5
import pandas as pd
import time, logging, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from datetime import datetime
from core.account import MT5Account
from core.order import OrderManager
from core.data_loader import DataLoader
from utils.notifier import Notifier
from utils.calculator import (
    calculate_lot_size,
    get_pip_value,
    calculate_take_profit,
    calculate_stop_loss,
)
# from strategies.indicator_strategy import IndicatorStrategy

# Load config từ .env
load_dotenv()
SYMBOL = os.getenv("TRADE_SYMBOL", "XAUUSD")
TIMEFRAME = getattr(mt5, f"TIMEFRAME_{os.getenv('TRADE_TIMEFRAME')}")
CANDLES = int(os.getenv("CANDLES"))
RISK_PERCENT = float(os.getenv("RISK_PERCENT"))
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

# Khởi tạo các đối tượng
account = MT5Account()
order_manager = OrderManager()
data_loader = DataLoader()
notifier = Notifier(WEBHOOK_URL)

# Đăng nhập account vào MetaTrader5
if not account.login():
    notifier.send_log(
        title="❌ MetaTrader5 connection failed.",
        description="Unable to log in to MetaTrader5 account.\nCheck your account information or Internet connection.",
        footer=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    exit()
notifier.send_log(
    title="✅ MetaTrader5 connection successfully.",
    description=f"Account login successfully.\nAccount: `{account.account}`\nServer: `{account.server}`\nBalance: `{account.get_balance()} USD`",
    footer=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
)

while True:
    df = data_loader.get_candles(SYMBOL, TIMEFRAME, CANDLES)
    if df is None or df.empty:
        continue

    print(df)
    exit()
    balance = account.get_balance()
    pip_value = get_pip_value(SYMBOL)
    print(balance)
    print(pip_value)
    exit()
#     logger.info("Đã ngắt kết nối MetaTrader5 trong DataLoader")
    # lot_size = calculate_lot_size(balance, RISK_PERCENT, stop_loss_pips, pip_value)
    # stop_loss = strategy.get_stop_loss_price()
    # take_profit = strategy.get_take_profit_price()
    # stop_loss_pips = abs(entry_price - stop_loss) / pip_value