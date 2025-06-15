import MetaTrader5 as mt5
import pandas as pd
import time, logging, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

from dotenv import load_dotenv
from datetime import datetime
from cores.account import MT5Account
from cores.order import OrderManager
from cores.data_loader import DataLoader
from strategies.simpleStrategy import SimpleStrategy
from utils.notifier import Notifier
from utils.calculator import (
    calculate_lot_size,
    get_pip_value,
    calculate_take_profit,
    calculate_stop_loss,
)

# Load config từ .env
load_dotenv()
SYMBOL = os.getenv("TRADE_SYMBOL", "BTCUSD")
TIMEFRAME = getattr(mt5, f"TIMEFRAME_{os.getenv('TRADE_TIMEFRAME', 'M1')}")
RR_RATIO = int(os.getenv("RR_RATIO", 2))
CANDLES = int(os.getenv("CANDLES", 200))
RISK_PERCENT = float(os.getenv("RISK_PERCENT", 1))
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

# Khởi tạo các đối tượng chính
account = MT5Account()
order_manager = OrderManager()
data_loader = DataLoader()
notifier = Notifier(WEBHOOK_URL)

# Đăng nhập MT5
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
    # Bỏ qua nếu đang có lệnh mở
    if order_manager.has_open_position(SYMBOL):
        logger.info("🔁 Đang có lệnh mở. Chờ...")
        time.sleep(10)
        continue

    # Lấy dữ liệu
    df = data_loader.get_candles(SYMBOL, TIMEFRAME, CANDLES)
    if df is None or df.empty:
        logger.error("❌ Không lấy được dữ liệu nến.")
        time.sleep(5)
        continue

    # Phân tích chiến lược
    strategy = SimpleStrategy(df)
    strategy.analyze()
    signal = strategy.get_signal()
    trade = strategy.get_trade_info()

    # print(df)
    if signal in ['buy', 'sell']:
        last = df.iloc[-1]
        balance = account.get_balance()
        print(balance)
        
        pip_value = get_pip_value(SYMBOL)

        sl = calculate_stop_loss(
            entry_price = trade['entry'],
            order_type = signal,
            atr = last['ATR'],
            # band = last['BB_LOWER'] if signal == 'buy' else last['BB_UPPER']
        )

        tp = calculate_take_profit(
            entry_price = trade['entry'],
            order_type = signal,
            atr = last['ATR'],
            rr_ratio = RR_RATIO
        )

        stop_loss_pips = abs(trade['entry'] - sl) / pip_value
        lot = calculate_lot_size(
            balance = balance,
            risk_percent = RISK_PERCENT,
            stop_loss_pips = stop_loss_pips,
            pip_value = pip_value
        )

        order_ticket = order_manager.place_order(
            symbol = SYMBOL,
            action = signal,
            volume = lot,
            take_profit = tp,
            stop_loss = sl
        )

        if order_ticket:
            notifier.send_log(
                title = f"🚀 {signal.upper()} ORDER PLACED",
                description = f"✅ Lệnh đã đặt:\nSymbol: `{SYMBOL}`\nEntry: `{trade['entry']}`\nLot: `{lot}`\nTP: `{tp}`\nSL: `{sl}`",
                footer = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            notifier.send_log(
                title = "⚠️ ORDER FAILED",
                description = f"❌ Gửi lệnh thất bại `{signal}` cho {SYMBOL}.",
                footer = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        time.sleep(10)