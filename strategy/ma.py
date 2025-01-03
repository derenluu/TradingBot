import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time

# Lấy dữ liệu nến (candlesticks)
def get_candlestick_data(symbol, timeframe, n_candles):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
    if rates is None:
        print("Failed to get candlestick data:", mt5.last_error())
        return None
    return pd.DataFrame(rates)

# Tính toán đường MA
def calculate_ma(data, period, column='close', method='sma'):
    if method == 'ema':
        return data[column].ewm(span=period, adjust=False).mean()
    else:
        return data[column].rolling(window=period).mean()
    
# Chiến lược MA
def ma_strategy(data, fast_period, slow_period):
    data['fast_ma'] = calculate_ma(data, fast_period, method='ema')
    data['slow_ma'] = calculate_ma(data, slow_period, method='ema')

    # Tín hiệu giao dịch: fast_ma cắt slow_ma
    data['signal'] = np.where(data['fast_ma'] > data['slow_ma'], 1, -1)
    data['crossover'] = data['signal'].diff()  # Phát hiện điểm giao cắt
    return data