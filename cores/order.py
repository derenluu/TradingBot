import MetaTrader5 as mt5
import logging
logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, deviation = 10, magic = 13122015):
            self.deviation = deviation
            self.magic = magic


    def place_order(self, symbol, action, volume, take_profit, stop_loss):
        symbol_tick = mt5.symbol_info_tick(symbol)
        if symbol_tick is None:
            logger.error(f"Không thể lấy thông tin giá cho {symbol}")
            return False

        if volume <= 0:
            print("Volume must be greater than 0")
            return False
        
        order_type = mt5.ORDER_TYPE_BUY if action.lower() == 'buy' else mt5.ORDER_TYPE_SELL
        order_price = symbol_tick.ask if order_type == mt5.ORDER_TYPE_BUY else symbol_tick.bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": order_price,
            "tp": take_profit,
            "sl": stop_loss,
            "deviation": self.deviation,
            "magic": self.magic,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Không thể gửi lệnh: {result.comment}")
            return False

        logger.info(f"Đã gửi lệnh thành công. Order ticket: {result.order}")
        return result.order


    def close_order(self, order_ticket):   
        positions = mt5.positions_get(ticket=order_ticket)
        if not positions:
            logger.error(f"Không tìm thấy lệnh với ticket: {order_ticket}. Lỗi: {mt5.last_error()}")
            return False

        position = positions[0]
        symbol = position.symbol

        symbol_tick = mt5.symbol_info_tick(symbol)
        if symbol_tick is None:
            logger.error(f"Không thể lấy giá hiện tại cho {symbol}")
            return False

        close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        close_price = symbol_tick.bid if close_type == mt5.ORDER_TYPE_SELL else symbol_tick.ask

        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": position.volume,
            "type": close_type,
            "position": order_ticket,
            "price": close_price,
            "deviation": self.deviation,
            "magic": getattr(position, 'magic', self.magic),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Đóng lệnh thất bại với ticket {order_ticket}: {result.comment}")
            return False

        logger.info(f"Đã đóng lệnh thành công: ticket {order_ticket}")
        return True
    
    
    def has_open_position(self, symbol):
        positions = mt5.positions_get(symbol = symbol)
        return positions is not None and len(positions) > 0


    def get_open_position_ticket(self, symbol):
        positions = mt5.positions_get(symbol=symbol)
        if not positions:
            return None
        return positions[0].ticket