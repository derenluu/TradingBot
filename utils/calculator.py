import MetaTrader5 as mt5
import logging
logger = logging.getLogger(__name__)


def calculate_lot_size(balance, risk_percent, stop_loss_pips, pip_value):
    if stop_loss_pips <= 0 or pip_value <= 0:
        raise ValueError("stop_loss_pips và pip_value phải lớn hơn 0")

    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    return round(lot_size, 2)


def get_pip_value(self, symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        logger.error(f"Không tìm thấy symbol: {symbol}")
        return None

    tick_size = symbol_info.trade_tick_size
    pip_size = tick_size * 10
    return pip_size


def calculate_stop_loss(self, entry_price, order_type, atr, band):
    if None in (entry_price, order_type, atr, band):
        return None

    if order_type.lower() == 'buy':
        return min(entry_price - atr, band)
    elif order_type.lower() == 'sell':
        return max(entry_price + atr, band)
    else:
        raise ValueError("order_type phải là 'buy' hoặc 'sell'")


def calculate_take_profit(self, entry_price, order_type, atr):
    if None in (entry_price, order_type, atr):
        return None

    if order_type.lower() == 'buy':
        return entry_price + atr * self.rr_ratio
    elif order_type.lower() == 'sell':
        return entry_price - atr * self.rr_ratio
    else:
        raise ValueError("order_type phải là 'buy' hoặc 'sell'")