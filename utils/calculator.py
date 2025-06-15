import MetaTrader5 as mt5
import logging
logger = logging.getLogger(__name__)


def calculate_lot_size(balance, risk_percent, stop_loss_pips, pip_value):
    if stop_loss_pips <= 0 or pip_value <= 0:
        raise ValueError("stop_loss_pips và pip_value phải lớn hơn 0")

    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    return round(lot_size, 2)


def get_pip_value(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        logger.error(f"Không tìm thấy symbol: {symbol}")
        return None

    tick_size = symbol_info.trade_tick_size
    pip_size = tick_size * 10
    return pip_size


def calculate_stop_loss(entry_price, order_type, atr):
    if any(x is None for x in (entry_price, order_type, atr)):
        return None

    order_type = order_type.lower()
    if order_type == 'buy':
        return entry_price - atr
    elif order_type == 'sell':
        return entry_price + atr
    else:
        raise ValueError("order_type phải là 'buy' hoặc 'sell'")


def calculate_take_profit(entry_price, order_type, atr, rr_ratio):
    if any(x is None for x in (entry_price, order_type, atr, rr_ratio)):
        return None

    order_type = order_type.lower()
    if order_type == 'buy':
        return entry_price + atr * rr_ratio
    elif order_type == 'sell':
        return entry_price - atr * rr_ratio
    else:
        raise ValueError("order_type phải là 'buy' hoặc 'sell'")