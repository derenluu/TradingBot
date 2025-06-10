def calculate_bollinger_bands(df, column = 'close', window = 15, num_std = 1.5):
    rolling_mean = df[column].rolling(window = window).mean()
    rolling_std = df[column].rolling(window = window).std()

    df['BB_MID'] = rolling_mean
    df['BB_UPPER'] = rolling_mean + (rolling_std * num_std)
    df['BB_LOWER'] = rolling_mean - (rolling_std * num_std)
    return df[['BB_UPPER', 'BB_MID', 'BB_LOWER']]


def get_stop_loss_from_bollinger(df, order_type = 'buy'):
    if df.empty or 'BB_LOWER' not in df.columns or 'BB_UPPER' not in df.columns:
        return None

    last = df.iloc[-1]

    if order_type == 'buy':
        return last['BB_LOWER']
    elif order_type == 'sell':
        return last['BB_UPPER']
    else:
        return None