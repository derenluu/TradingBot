def calculate_ema(df, column = 'close', span = 14):
    ema_column = f'EMA_{span}'
    df[ema_column] = df[column].ewm(span = span, adjust = False).mean()
    return df[ema_column]