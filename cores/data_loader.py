import MetaTrader5 as mt5
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Lớp hỗ trợ lấy dữ liệu từ MetaTrader 5, bao gồm dữ liệu nến và dữ liệu lịch sử khác
class DataLoader:
    def __init__(self):
        if not mt5.initialize():
            logger.error("Không thể khởi tạo kết nối MT5: %s", mt5.last_error())
            raise Exception("MT5 initialize failed")
        else:
            logger.info("✅ MT5 đã được khởi tạo thành công")

    # Lấy dữ liệu nến gần nhất
    # Parameters:
    # ⇒ symbol: mã giao dịch (e.g. 'BTCUSD')
    # ⇒ timeframe: khung thời gian (e.g. mt5.TIMEFRAME_M5)
    # ⇒ n_candles: số lượng nến cần lấy
    # Returns:
    # ⇒ pandas DataFrame nếu thành công
    # ⇒ None nếu thất bại
    def get_candles(self, symbol, timeframe, n_candles):
        bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
        if bars is None:
            logger.error(f"Lỗi lấy dữ liệu nến cho {symbol}: {mt5.last_error()}")
            return None

        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    # Lấy dữ liệu nến từ thời gian 'start' đến 'end'
    # Parameters:
    # ⇒ start, end: datetime.datetime
    def get_candles_from_to(self, symbol, timeframe, start, end):
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y-%m-%d")
        if isinstance(end, str):
            end = datetime.strptime(end, "%Y-%m-%d")

        bars = mt5.copy_rates_range(symbol, timeframe, start, end)
        if bars is None:
            logger.error(f"Lỗi lấy dữ liệu nến theo thời gian cho {symbol}: {mt5.last_error()}")
            return None

        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    # Ngắt kết nối MetaTrader5
    def shutdown(self):
        mt5.shutdown()
        logger.info("Đã ngắt kết nối MetaTrader5 trong DataLoader")
