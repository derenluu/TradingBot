import MetaTrader5 as mt5
import logging
import os
from dotenv import load_dotenv
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
ACCOUNT = int(os.getenv("MT5_ACCOUNT"))
PASSWORD = str(os.getenv("MT5_PASSWORD"))
SERVER = str(os.getenv("MT5_SERVER"))

class MT5Account:
    def __init__(self, account = ACCOUNT, password = PASSWORD, server = SERVER):
        self.account = account
        self.password = password
        self.server = server
        self.logged_in = False


    def login(self):
        if not mt5.initialize():
            logger.error("Không thể khởi tạo MT5: %s", mt5.last_error())
            return False

        if not mt5.login(self.account, password = self.password, server = self.server):
            logger.error("Đăng nhập thất bại: %s", mt5.last_error())
            return False

        self.logged_in = True
        logger.info(f"Đăng nhập thành công tài khoản {self.account} trên server {self.server}")
        return True


    def logout(self):
        mt5.shutdown()
        self.logged_in = False
        logger.info("Đã đăng xuất khỏi MetaTrader 5")

    
    def get_balance(self):
        if not self.logged_in:
            logger.warning("Chưa đăng nhập. Không thể lấy số dư.")
            return None
        info = mt5.account_info()
        return info.balance if info else None


    def get_equity(self):
        if not self.logged_in:
            logger.warning("Chưa đăng nhập. Không thể lấy thông tin equity.")
            return None
        info = mt5.account_info()
        return info.equity if info else None


    def get_orders(self):
        orders = mt5.orders_get()
        if orders is None:
            logger.warning("Không có lệnh đang mở. Lỗi: %s", mt5.last_error())
            return []
        return orders


    def get_trades(self):
        trades = mt5.history_orders_get()
        if trades is None:
            logger.warning("Không thể lấy lịch sử giao dịch: %s", mt5.last_error())
            return []
        return trades


    def get_account_info(self):
        info = mt5.account_info()
        if info:
            return info._asdict()
        logger.warning("Không thể lấy thông tin tài khoản.")
        return {}
