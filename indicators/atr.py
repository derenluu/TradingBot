def calculate_atr(df, period = 7):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift(1)).abs()
    low_close = (df['low'] - df['close'].shift(1)).abs()

    tr = high_low.to_frame('hl')
    tr['hc'] = high_close
    tr['lc'] = low_close

    df['tr'] = tr.max(axis = 1)
    df['ATR'] = df['tr'].ewm(span = period, min_periods = period).mean()
    df.drop(columns = ['tr'], inplace = True)
    return df['ATR']