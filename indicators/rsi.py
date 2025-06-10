def calculate_rsi(df, column = 'close', period = 16):
    delta = df[column].diff()
    gain = delta.where(delta > 0, 0.0).rolling(window = period).mean()
    loss = -delta.where(delta < 0, 0.0).rolling(window = period).mean()

    rs = gain / loss
    rsi_column = f'RSI'
    df[rsi_column] = 100 - (100 / (1 + rs))
    return df[rsi_column]