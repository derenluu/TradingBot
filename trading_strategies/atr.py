def ATR_Calc(df, period=14):
    if not {'high', 'low', 'close'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'high', 'low', 'close' columns")

    df['high-low'] = df['high'] - df['low']
    df['high-close'] = abs(df['high'] - df['close'].shift(1))
    df['low-close'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['high-low', 'high-close', 'low-close']].max(axis=1)
    df.loc[:, 'ATR'] = df['TR'].ewm(span=period, min_periods=period).mean()
    df.drop(['high-low', 'high-close', 'low-close', 'TR'], axis=1, inplace=True)
    return df['ATR']