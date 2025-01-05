import MetaTrader5 as mt5

def Pip_Calc(symbol):
    """
    Function to retrieve the pip size of a symbol from MetaTrader 5
    :param symbol: string of the symbol to be queried
    :return: float of the pip size
    """
    # Get the symbol information
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"{symbol} information not found")
        mt5.shutdown()
        return None
    
    tick_size = symbol_info.trade_tick_size
    pip_size = tick_size * 10
    return pip_size
