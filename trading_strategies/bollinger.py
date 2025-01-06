def Bollinger_Calc(df, column='close', window=20, num_of_std=2):
    rolling_mean = df[column].rolling(window=window).mean()
    rolling_std = df[column].rolling(window=window).std()
    df.loc[:, 'upper_band'] = rolling_mean + (rolling_std * num_of_std)
    df.loc[:, 'middle_band'] = rolling_mean
    df.loc[:, 'lower_band'] = rolling_mean - (rolling_std * num_of_std)
    return df[['upper_band', 'middle_band', 'lower_band']]