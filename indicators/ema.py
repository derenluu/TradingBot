# Tính Exponential Moving Average (EMA) và thêm vào DataFrame
# Parameters:
# ⇒ df (pd.DataFrame): Dữ liệu OHLCV
# ⇒ column (str): Cột giá dùng để tính toán EMA
# ⇒ span (int): Số chu kỳ tính EMA
# Returns:
# ⇒ pd.Series: Cột EMA vừa được thêm vào df (df[f'EMA_{span}'])
def calculate_ema(df, column = 'close', span = 14):
    ema_column = f'EMA_{span}'
    df[ema_column] = df[column].ewm(span = span, adjust = False).mean()
    return df[ema_column]