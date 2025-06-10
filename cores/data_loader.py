import MetaTrader5 as mt5
import pandas as pd
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        if not mt5.initialize():
            logger.error("Không thể khởi tạo kết nối MT5: %s", mt5.last_error())
            raise Exception("MT5 initialize failed")
        else:
            logger.info("✅ MT5 đã được khởi tạo thành công")


    def get_candles(self, symbol, timeframe, n_candles):
        bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
        if bars is None:
            logger.error(f"Lỗi lấy dữ liệu nến cho {symbol}: {mt5.last_error()}")
            return None

        df = pd.DataFrame(bars)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.rename(columns = {'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 'tick_volume': 'volume'}, inplace = True)
        return df


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
        df.rename(columns = {'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close', 'tick_volume': 'volume'}, inplace = True)
        return df


    def get_latest_candle(self, symbol, timeframe):
        return self.get_candles(symbol, timeframe, 1).iloc[-1]


    def shutdown(self):
        mt5.shutdown()
        logger.info("Đã ngắt kết nối MetaTrader5 trong DataLoader")
