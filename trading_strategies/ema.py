def EMA_Calc(df, column='close', span=14):
    df.loc[:, 'EMA'] = df[column].ewm(span=span, adjust=False).mean()
    return df['EMA']