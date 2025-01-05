import MetaTrader5 as mt5

# Place order function
def Place_Order(symbol, action, volume, take_profit, stop_loss):
    """Places a buy or sell order with specified parameters."""

    # Determine order type and price based on action
    order_type = mt5.ORDER_TYPE_BUY if action == 'buy' else mt5.ORDER_TYPE_SELL
    order_price = mt5.symbol_info_tick(symbol).ask if action == 'buy' else mt5.symbol_info_tick(symbol).bid

    # Create the order request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": order_price,
        "tp": take_profit,
        "sl": stop_loss,
        "deviation": 10,
        "magic": 13122015,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send the order request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order send failed. Error: {result.comment}")
        return False
    print(f"Order {result.order} placed successfully")
    return result.order

# Close order function
def Close_Order(order_ticket):
    """Closes the specified order by its ticket."""
    
    # Retrieve the position by ticket
    position = mt5.positions_get(ticket=order_ticket)
    if not position:
        print(f"Order not found for ticket: {order_ticket}, Error: {mt5.last_error()}")
        return False

    position = position[0]
    symbol = position.symbol

    # Determine close order type and price
    close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
    close_price = mt5.symbol_info_tick(symbol).bid if close_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(symbol).ask

    # Create the close request
    close_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": position.volume,
        "type": close_type,
        "position": order_ticket,
        "price": close_price,
        "deviation": 10,
        "magic": position.magic,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Send the close request
    result = mt5.order_send(close_request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Close order failed for ticket {order_ticket}: {result.comment}")
        return False
    print(f"Order {order_ticket} closed successfully")
    return True
   