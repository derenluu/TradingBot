def SMA_Calc(df, column='close', window=14):
    df.loc[:, 'SMA'] = df[column].rolling(window=window).mean()
    return df['SMA']