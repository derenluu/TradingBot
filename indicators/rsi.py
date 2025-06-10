# Tính Relative Strength Index (RSI) và thêm vào DataFrame
# Parameters:
# ⇒ df (pd.DataFrame): Dữ liệu OHLCV
# ⇒ column (str): Cột giá để tính toán RSI
# ⇒ period (int): Chu kỳ tính RSI (default = 14)
# Returns:
# ⇒ pd.Series: Cột RSI vừa được thêm vào df (df[f'RSI_{period}'])
def calculate_rsi(df, column = 'close', period = 14):
    delta = df[column].diff()
    gain = delta.where(delta > 0, 0.0).rolling(window = period).mean()
    loss = -delta.where(delta < 0, 0.0).rolling(window = period).mean()

    rs = gain / loss
    rsi_column = f'RSI_{period}'
    df[rsi_column] = 100 - (100 / (1 + rs))
    return df[rsi_column]