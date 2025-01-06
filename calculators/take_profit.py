def TakeProfit_Calc(entry_price, order_type, atr, risk_reward_ratio=2):
    """
    Calculate the take profit price based on entry price, order type, and ATR.
    
    :param entry_price: Entry price of the order.
    :param order_type: 'buy' or 'sell'.
    :param atr: Average True Range value.
    :param risk_reward_ratio: Ratio of reward to risk, default is 2.
    :return: Calculated take profit price.
    """
    if order_type == 'buy':
        # For buy orders, take profit is above the entry price
        take_profit = entry_price + (atr * risk_reward_ratio)
    elif order_type == 'sell':
        # For sell orders, take profit is below the entry price
        take_profit = entry_price - (atr * risk_reward_ratio)
    return take_profit