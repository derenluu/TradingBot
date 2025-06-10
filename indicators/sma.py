def calculate_sma(df, column = 'close', window = 14):
    sma_column = f'SMA_{window}'
    df[sma_column] = df[column].rolling(window = window).mean()
    return df[sma_column]