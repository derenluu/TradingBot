import os
from dotenv import load_dotenv
from binance.cm_futures import CMFutures

# Load biến môi trường
load_dotenv()

# Lấy API Key và Secret từ file .env
key = os.getenv("BINANCE_API")
secret = os.getenv("BINANCE_SECRET")

BASE_URL = "https://fapi.binance.com"

# Khởi tạo client với API Key và Secret
cm_futures_client = CMFutures(key=key, secret=secret)

# Lấy thông tin tài khoản
account_info = cm_futures_client.account()

print(f"Account information: {account_info['assets']}")
