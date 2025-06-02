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
from indicators.atr import calculate_atr
from indicators.bollinger import calculate_bollinger_bands
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

# Đăng nhập account thành công MetaTrader5
notifier.send_log(
    title="✅ MetaTrader5 connection successfully.",
    description=f"Account login successfully.\nAccount: `{account.account}`\nServer: `{account.server}`\nBalance: `{account.get_balance()} USD`",
    footer=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
)

while True:
    # Kiểm tra đảm bảo rằng đang không có lệnh nào đang mở
    if order_manager.has_open_position():
        print("🔁 Đang có lệnh mở, không thực hiện thêm lệnh mới.")
        time.sleep(1)
        continue

    # Lấy data real time
    df = data_loader.get_candles(SYMBOL, TIMEFRAME, CANDLES)
    if df is None or df.empty:
        print("❌ Không lấy được dữ liệu để hiển thị.")
        continue

    balance = account.get_balance()
    pip_value = get_pip_value(SYMBOL)

    sub_df = df.copy()
    strategy = SimpleStrategy(sub_df)
    strategy.analyze()
    signal = strategy.get_signal()
    trade = strategy.get_trade_info()

    logger.info(f" Signal: {SYMBOL} - {signal}")

    if signal in ['buy', 'sell']:
        calculate_bollinger_bands(sub_df, window = 20)
        calculate_atr(sub_df, period = 14)
        last = sub_df.iloc[-1]

        sl = calculate_stop_loss(trade['entry'], signal, last['ATR'], last['boll_lower'] if signal == 'buy' else last['boll_upper'])
        tp = calculate_take_profit(trade['entry'], signal, last['ATR'])
        stop_loss_pips = abs(trade['entry'] - sl) / pip_value
        lot = calculate_lot_size(balance, risk_percent = RISK_PERCENT, stop_loss_pips = stop_loss_pips, pip_value = pip_value)

        order_ticket = order_manager.place_order(
            symbol = SYMBOL,
            action = signal,
            volume = lot,
            take_profit = tp,
            stop_loss = sl
        )

        if order_ticket:
            notifier.send_log(
                title=f"🚀 {signal.upper()} ORDER PLACED",
                description=f"Place order successfully.\nSymbol: `{SYMBOL}`\nEntry: `{trade['entry']}`\nLot: `{lot}`\nTP: `{tp}`\nSL: `{sl}`",
                footer=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            notifier.send_log(
                title="⚠️ ORDER FAILED",
                description=f"Order failed `{signal}` for {SYMBOL}.",
                footer=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    time.sleep(1)
        