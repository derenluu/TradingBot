import time, logging, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger(__name__)

from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi

class SimpleStrategy:
    def __init__(self, df):
        self.df = df
        self.entry_price = None
        self.order_type = None

    def analyze(self):
        calculate_sma(self.df, window = 8)
        calculate_sma(self.df, window = 89)
        # calculate_rsi(self.df, period = 14)

    def get_signal(self):
        if len(self.df) < 201:
            return 'hold'

        fast_sma = self.df['SMA_8']
        slow_sma = self.df['SMA_89']
        # rsi = self.df['RSI_14']
        close = self.df.iloc[-1]['close']

        # and rsi.iloc[-1] < 30
        if fast_sma.iloc[-2] < slow_sma.iloc[-2] and fast_sma.iloc[-1] > slow_sma.iloc[-1]:
            self.order_type = 'buy'
            self.entry_price = close
            return 'buy'

        # and rsi.iloc[-1] > 70
        elif fast_sma.iloc[-2] > slow_sma.iloc[-2] and fast_sma.iloc[-1] < slow_sma.iloc[-1]:
            self.order_type = 'sell'
            self.entry_price = close
            return 'sell'

        return 'hold'

    def get_trade_info(self):
        return {
            'type': self.order_type,
            'entry': self.entry_price
        }