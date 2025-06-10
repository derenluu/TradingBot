import time, logging, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger(__name__)

from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi
from indicators.atr import calculate_atr
from indicators.bollinger import calculate_bollinger_bands

class SimpleStrategy:
    def __init__(self, df):
        self.df = df
        self.entry_price = None
        self.order_type = None


    def analyze(self):
        calculate_atr(self.df, period = 14)
        calculate_rsi(self.df, period = 14)
        calculate_bollinger_bands(self.df, column = 'close', window = 30, num_std = 2)

        # Tính độ rộng Bollinger Band
        self.df['bb_width'] = (self.df['boll_upper'] - self.df['boll_lower']) / self.df['boll_middle']


    def get_signal(self):
        # Dùng 34 cây nến, vừa đủ data cho BB 30 + RSI 14
        if len(self.df) < 35:
            return 'hold'

        last = self.df.iloc[-1]

        # Điều kiện BUY: giá > BB mid, RSI > 50, BB hẹp
        if (last['close'] > last['boll_middle'] and last['RSI_14'] > 50 and last['bb_width'] < 0.12):
            self.order_type = 'buy'
            self.entry_price = last['close']
            return 'buy'

        # Điều kiện SELL: giá < BB mid, RSI < 50, BB hẹp
        elif ( last['close'] < last['boll_middle'] and last['RSI_14'] < 50 and last['bb_width'] < 0.12):
            self.order_type = 'sell'
            self.entry_price = last['close']
            return 'sell'
        
        return 'hold'


    def get_trade_info(self):
        atr = self.df.iloc[-1]['ATR']
        tp = self.entry_price + 3 * atr if self.order_type == 'buy' else self.entry_price - 3 * atr
        sl = self.entry_price - 1.5 * atr if self.order_type == 'buy' else self.entry_price + 1.5 * atr

        return {
            'type': self.order_type,
            'entry': self.entry_price
        }