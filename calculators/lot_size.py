def Lot_Calc(balance, risk_percent, stop_loss_pips, pip_value):
    """
    Function to calculate a lot size (or volume) based on risk management principles.
    The balance is passed as a static amount, any compounding is taken care of in the parent function.
    
    :param balance: float of the balance being risked
    :param risk_percent: float of the amount to risk (in percentage)
    :param stop_loss_pips: float of the stop loss in pips
    :param pip_value: float of the pip value for the pair (in account currency)
    :return: float of the lot_size (rounded to two decimal places)
    """
    
    # Step 1: Calculate the amount of money to risk
    risk_amount = balance * (risk_percent / 100)
    
    # Step 2: Calculate lot size based on risk amount and stop loss in pips
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    
    # Round lot size to the nearest 0.01 (standard lot size precision)
    return round(lot_size, 2)
