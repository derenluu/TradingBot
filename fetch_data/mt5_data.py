import MetaTrader5 as mt5
import pandas as pd

def Data_Candles(symbol, timeframe, n_candles):
    """
    Retrieve candlestick data from MetaTrader 5.
    
    :param symbol: Trading symbol (e.g., 'BTCUSD').
    :param timeframe: Timeframe (e.g., mt5.TIMEFRAME_M1).
    :param n_candles: Number of candles to retrieve.
    :return: DataFrame containing candlestick data or None if retrieval fails.
    """
    # Retrieve bars from MT5
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
    if bars is None:
        print(f"Failed to retrieve data for {symbol}: {mt5.last_error()}")
        return None

    # Convert to DataFrame and format time column
    df = pd.DataFrame(bars)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df