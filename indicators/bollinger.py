# Tính Bollinger Bands và thêm vào DataFrame
# Parameters:
# ⇒ df (pd.DataFrame): Dữ liệu OHLCV
# ⇒ column (str): Cột giá để tính toán
# ⇒ window (int): Số chu kỳ SMA
# ⇒ num_std (int): Hệ số độ lệch chuẩn
# Returns:
# ⇒ pd.DataFrame: DataFrame chứa cột 'boll_upper', 'boll_middle', 'boll_lower'
def calculate_bollinger_bands(df, column = 'close', window = 20, num_std = 2):
    rolling_mean = df[column].rolling(window = window).mean()
    rolling_std = df[column].rolling(window = window).std()

    df['boll_middle'] = rolling_mean
    df['boll_upper'] = rolling_mean + (rolling_std * num_std)
    df['boll_lower'] = rolling_mean - (rolling_std * num_std)
    return df[['boll_upper', 'boll_middle', 'boll_lower']]

# Xác định giá Stop Loss dựa trên Bollinger Band
# Parameters:
# ⇒ df (pd.DataFrame): DataFrame đã tính Bollinger Bands
# ⇒ order_type (str): 'buy' hoặc 'sell'
# Returns:
# ⇒ float: Giá stop loss từ boll_upper hoặc boll_lower tuỳ theo loại lệnh
def get_stop_loss_from_bollinger(df, order_type='buy'):
    if df.empty or 'boll_lower' not in df.columns or 'boll_upper' not in df.columns:
        return None

    last = df.iloc[-1]

    if order_type == 'buy':
        return last['boll_lower']
    elif order_type == 'sell':
        return last['boll_upper']
    else:
        return None