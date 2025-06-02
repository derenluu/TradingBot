# Tính Simple Moving Average (SMA) và thêm vào DataFrame
# Parameters:
# ⇒ df (pd.DataFrame): Dữ liệu nến OHLCV
# ⇒ column (str): Cột giá để tính trung bình (default = 'close')
# ⇒ window (int): Số chu kỳ để tính SMA (default = 14)
# Returns:
# ⇒ pd.Series: Cột SMA vừa được thêm vào df (df[f'SMA_{window}'])
def calculate_sma(df, column = 'close', window = 14):
    sma_column = f'SMA_{window}'
    df[sma_column] = df[column].rolling(window = window).mean()
    return df[sma_column]