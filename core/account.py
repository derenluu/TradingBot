import MetaTrader5 as mt5
import logging
import os
from dotenv import load_dotenv

# Thiết lập logging để theo dõi tiến trình và lỗi
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Load biến môi trường từ file .env (tài khoản, mật khẩu, server)
load_dotenv()
ACCOUNT = int(os.getenv("MT5_ACCOUNT"))
PASSWORD = str(os.getenv("MT5_PASSWORD"))
SERVER = str(os.getenv("MT5_SERVER"))

# Lớp quản lý kết nối với tài khoản MetaTrader 5,
# bao gồm đăng nhập, lấy thông tin tài khoản, số dư, lệnh, ...
class MT5Account:
    def __init__(self, account = ACCOUNT, password = PASSWORD, server = SERVER):
        self.account = account
        self.password = password
        self.server = server
        self.logged_in = False

    # Đăng nhập vào MetaTrader 5
    # Trả về True nếu đăng nhập thành công
    # Trả về False nếu thất bại
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

    # Đăng xuất khỏi MetaTrader 5
    def logout(self):
        mt5.shutdown()
        self.logged_in = False
        logger.info("Đã đăng xuất khỏi MetaTrader 5")

    # Lấy số dư tài khoản hiện tại
    # Trả về số dư nếu đăng nhập hợp lệ
    # Trả về None nếu chưa đăng nhập hoặc không thể truy xuất
    def get_balance(self):
        if not self.logged_in:
            logger.warning("Chưa đăng nhập. Không thể lấy số dư.")
            return None
        info = mt5.account_info()
        return info.balance if info else None

    # Lấy equity (tài sản ròng hiện tại) của tài khoản
    # Trả về giá trị equity nếu có
    # Trả về None nếu chưa đăng nhập hoặc gặp lỗi
    def get_equity(self):
        if not self.logged_in:
            logger.warning("Chưa đăng nhập. Không thể lấy thông tin equity.")
            return None
        info = mt5.account_info()
        return info.equity if info else None

    # Lấy danh sách các lệnh đang mở
    # Trả về danh sách lệnh
    # Trả về [] nếu không có hoặc gặp lỗi
    def get_orders(self):
        orders = mt5.orders_get()
        if orders is None:
            logger.warning("Không có lệnh đang mở. Lỗi: %s", mt5.last_error())
            return []
        return orders

    # Lấy danh sách các lệnh đã hoàn tất trong lịch sử
    # Trả về danh sách lệnh
    # Trả về [] nếu gặp lỗi
    def get_trades(self):
        trades = mt5.history_orders_get()
        if trades is None:
            logger.warning("Không thể lấy lịch sử giao dịch: %s", mt5.last_error())
            return []
        return trades

    # Lấy tất cả thông tin tài khoản dưới dạng dict
    # Trả về dict nếu thành công
    # Trả về {} nếu gặp lỗi
    def get_account_info(self):
        info = mt5.account_info()
        if info:
            return info._asdict()
        logger.warning("Không thể lấy thông tin tài khoản.")
        return {}
