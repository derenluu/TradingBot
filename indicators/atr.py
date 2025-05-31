#  Tính Average True Range (ATR) và thêm vào DataFrame sử dụng EWM (phản ứng nhanh - phù hợp M1)
# Parameters:
# ⇒ df (pd.DataFrame): Dữ liệu nến OHLCV, phải có 'high', 'low', 'close'
# ⇒ period (int): Số chu kỳ để tính ATR (default = 14)
# Returns:
# ⇒pd.Series: Cột ATR vừa được thêm vào df (df['ATR'])
def calculate_atr(df, period = 14):
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift(1)).abs()
    low_close = (df['low'] - df['close'].shift(1)).abs()

    tr = high_low.to_frame('hl')
    tr['hc'] = high_close
    tr['lc'] = low_close

    df['TR'] = tr.max(axis = 1)
    df['ATR'] = df['TR'].ewm(span = period, min_periods = period).mean()
    df.drop(columns=['TR'], inplace = True)
    return df['ATR']