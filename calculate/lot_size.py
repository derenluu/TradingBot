def Calculator_Lot(balance, risk_percent, stop_loss_pips, pip_value):
    """
    Tính kích thước lot dựa trên rủi ro.
    
    :param balance: Số dư tài khoản
    :param risk_percent: Tỷ lệ rủi ro (%)
    :param stop_loss_pips: Khoảng cách Stop Loss (pips)
    :param pip_value: Giá trị mỗi pip (USD/pip)
    :return: Kích thước lot
    """
    risk_amount = balance * (risk_percent / 100)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    return round(lot_size, 2)