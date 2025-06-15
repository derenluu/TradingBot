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
        # calculate_rsi(self.df, period = 16)
        calculate_sma(self.df, window = 8)
        calculate_sma(self.df, window = 89)
        calculate_atr(self.df, period = 14)
        # calculate_bollinger_bands(self.df, column = 'close', window = 15, num_std = 1.5)

        # Tính độ rộng Bollinger Band
        # self.df['BB_WIDTH'] = (self.df['BB_UPPER'] - self.df['BB_LOWER']) / self.df['BB_MID']


    def get_signal(self):
        if len(self.df) < 100:
            return 'hold'

        # last = self.df.iloc[-1]

        fast_sma = self.df['SMA_8']
        slow_sma = self.df['SMA_89']

        prev_fast = fast_sma.iloc[-2]
        prev_slow = slow_sma.iloc[-2]
        curr_fast = fast_sma.iloc[-1]
        curr_slow = slow_sma.iloc[-1]

        last_close = self.df.iloc[-1]['close']
        self.entry_price = last_close

        # BUY khi SMA8 cắt lên SMA89
        if prev_fast < prev_slow and curr_fast > curr_slow:
            self.order_type = 'buy'
            return 'buy'
        # SELL khi SMA8 cắt xuống SMA89
        elif prev_fast > prev_slow and curr_fast < curr_slow:
            self.order_type = 'sell'
            return 'sell'
        

        # Điều kiện BUY: giá > BB mid, RSI > 50, BB hẹp
        # if (last['close'] > last['BB_MID'] and last['RSI'] > 50 and last['BB_WIDTH'] < 0.12):
        #     self.order_type = 'buy'
        #     self.entry_price = last['close']
        #     return 'buy'
        
        # Điều kiện SELL: giá < BB mid, RSI < 50, BB hẹp
        # elif (last['close'] < last['BB_MID'] and last['RSI'] < 50 and last['BB_WIDTH'] < 0.12):
        #     self.order_type = 'sell'
        #     self.entry_price = last['close']
        #     return 'sell'
        
        return 'hold'


    def get_trade_info(self):
        if self.entry_price is None or self.order_type is None:
            return None
    
        atr = self.df.iloc[-1]['ATR']
        if self.order_type == 'buy':
            sl = self.entry_price - 1.5 * atr
            tp = self.entry_price + 3 * atr
        else:
            sl = self.entry_price + 1.5 * atr
            tp = self.entry_price - 3 * atr

        return {
            'type': self.order_type,
            'entry': self.entry_price,
            'tp': tp,
            'sl': sl
        }