import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

# Tính toán khối lượng lot theo quản lý rủi ro
# Parameters:
# ⇒ balance (float): Số dư tài khoản
# ⇒ risk_percent (float): Tỷ lệ % rủi ro
# ⇒ stop_loss_pips (float): Khoảng SL tính bằng pips
# ⇒ pip_value (float): Giá trị 1 pip (theo đồng tiền tài khoản)
# Returns:
# ⇒ float: Lot size (làm tròn 2 chữ số)
def calculate_lot_size(balance, risk_percent, stop_loss_pips, pip_value):
    if stop_loss_pips <= 0 or pip_value <= 0:
        raise ValueError("stop_loss_pips và pip_value phải lớn hơn 0")

    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    return round(lot_size, 2)

# Tính kích thước pip cho một cặp tiền
# Parameters:
# ⇒ symbol (str): Tên cặp giao dịch (e.g. 'EURUSD')
# Returns:
# ⇒ float | None: Kích thước pip
def get_pip_value(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        logger.error(f"Không tìm thấy symbol: {symbol}")
        return None

    tick_size = symbol_info.trade_tick_size
    pip_size = tick_size * 10
    logger.info(f" {symbol} - Tick size: {tick_size}, Pip size: {pip_size}")
    return pip_size

# Tính giá Stop Loss dựa trên ATR và Bollinger Band
# Parameters:
# ⇒ entry_price (float): Giá vào lệnh
# ⇒ order_type (str): 'buy' hoặc 'sell'
# ⇒ atr (float): Giá trị ATR hiện tại
# ⇒ band (float): Giá trị dải Bollinger Band (trên/dưới)
# Returns:
# ⇒ float | None: Giá stop loss
def calculate_stop_loss(entry_price, order_type, atr, band):
    if None in (entry_price, order_type, atr, band):
        return None

    if order_type.lower() == 'buy':
        return min(entry_price - atr, band)
    elif order_type.lower() == 'sell':
        return max(entry_price + atr, band)
    else:
        raise ValueError("order_type phải là 'buy' hoặc 'sell'")

# Tính giá Take Profit dựa trên ATR và tỉ lệ RR
# Parameters:
# ⇒ entry_price (float): Giá vào lệnh
# ⇒ order_type (str): 'buy' hoặc 'sell'
# ⇒ atr (float): Giá trị ATR
# ⇒ rr_ratio (float): Tỉ lệ Reward/Risk (mặc định = 2)
# Returns:
# ⇒ float | None: Giá take profit
def calculate_take_profit(entry_price, order_type, atr, rr_ratio = 2):
    if None in (entry_price, order_type, atr):
        return None
    
    if order_type.lower() == 'buy':
        return entry_price + (atr * rr_ratio)
    elif order_type.lower() == 'sell':
        return entry_price - (atr * rr_ratio)
    else:
        raise ValueError("order_type phải là 'buy' hoặc 'sell'")