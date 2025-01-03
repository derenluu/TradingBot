import MetaTrader5 as mt5

def Login(account, password, server):
    """Login to MetaTrader 5"""
    if not mt5.initialize():
        print("Error initializing MT5:", mt5.last_error())
        return False
    
    if not mt5.login(account, password=password, server=server):
        print("Login error:", mt5.last_error())
        mt5.shutdown()
        return False

    print(f"Login successful: Account {account} on server {server}")
    return True

def Get_Balance():
    """Get account balance"""
    account_info = mt5.account_info()
    if account_info is None:
        print("Failed to get account info:", mt5.last_error())
        return None
    
    return account_info.balance

def Get_Equity():
    """Get account equity"""
    account_info = mt5.account_info()
    if account_info is None:
        print("Failed to get account info:", mt5.last_error())
        return None
    
    return account_info.equity

def Get_Orders():
    """Get the list of current orders"""
    orders = mt5.orders_get()
    if orders is None:
        print("Failed to get orders:", mt5.last_error())
        return []
    
    return orders

def Get_Trades():
    """Get the list of completed trades"""
    trades = mt5.history_orders_get()
    if trades is None:
        print("Failed to get trades:", mt5.last_error())
        return []
    
    return trades

def Place_Order(symbol, action, volume, price=None, stop_loss=None, take_profit=None):
    """Place an order (buy/sell)"""
    if action not in ['buy', 'sell']:
        print("Invalid action. Use 'buy' or 'sell'.")
        return False
    
    # Define order parameters
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if action == 'buy' else mt5.ORDER_TYPE_SELL,
        "price": price or mt5.symbol_info_tick(symbol).ask if action == 'buy' else mt5.symbol_info_tick(symbol).bid,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python trading bot order",
        "type_filling": mt5.ORDER_FILLING_IOC,
        "type_time": mt5.ORDER_TIME_GTC,
    }

    # Send the order
    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order failed:", result.comment)
        return False
    
    print(f"Order placed successfully: {action} {symbol} volume {volume}")
    return True

def Close_Order(order_ticket):
    """Close a specific order"""
    order = mt5.order_select(order_ticket)
    if not order:
        print("Order not found:", mt5.last_error())
        return False
    
    # Prepare close request
    close_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.symbol,
        "volume": order.volume,
        "type": mt5.ORDER_TYPE_SELL if order.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
        "position": order_ticket,
        "price": mt5.symbol_info_tick(order.symbol).bid if order.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(order.symbol).ask,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python trading bot close order",
        "type_filling": mt5.ORDER_FILLING_IOC,
        "type_time": mt5.ORDER_TIME_GTC,
    }

    # Send the close request
    result = mt5.order_send(close_request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Close order failed:", result.comment)
        return False
    
    print(f"Order {order_ticket} closed successfully")
    return True

def Logout():
    """Logout from MT5"""
    mt5.shutdown()
    print("Logged out from MetaTrader 5")
