def StopLoss_Calc(entry_price, order_type, atr, band):
    """
    Calculate the stop loss price based on entry price, order type, ATR, and Bollinger Bands.
    
    :param entry_price: Entry price of the order.
    :param order_type: 'buy' or 'sell'.
    :param atr: Average True Range value.
    :param band: Bollinger Band (upper or lower) relevant to the order type.
    :return: Calculated stop loss price.
    """
    if order_type == 'buy':
        # For buy orders, stop loss is below the entry price
        stop_loss = min(entry_price - atr, band)
    elif order_type == 'sell':
        # For sell orders, stop loss is above the entry price
        stop_loss = max(entry_price + atr, band)
    return stop_loss
    