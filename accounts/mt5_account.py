import MetaTrader5 as mt5

def Login(account, password, server):
    """Login to MetaTrader 5"""
    mt5.initialize()
    mt5.login(account, password=password, server=server)
    print(f"Login successful: Account {account} on server {server}")
    return True

def Get_Balance():
    """Get account balance"""
    account_info = mt5.account_info()
    return account_info.balance

def Get_Equity():
    """Get account equity"""
    account_info = mt5.account_info()    
    return account_info.equity

def Get_Orders():
    """Get the list of current orders"""
    orders = mt5.orders_get()    
    return orders

def Get_Trades():
    """Get the list of completed trades"""
    trades = mt5.history_orders_get()
    if trades is None:
        print("Failed to get trades:", mt5.last_error())
        return []
    
    return trades

def Logout():
    """Logout from MT5"""
    mt5.shutdown()
    print("Logged out from MetaTrader 5")
