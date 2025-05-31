import MetaTrader5 as mt5
import pandas as pd
import time, logging, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from datetime import datetime
from core.account import MT5Account
from core.order import OrderManager
from core.data_loader import DataLoader
from utils.notifier import Notifier
from utils.calculator import (
    calculate_lot_size,
    get_pip_value,
    calculate_take_profit,
    calculate_stop_loss,
)
from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi
from indicators.bollinger import calculate_bollinger_bands, get_stop_loss_from_bollinger
from indicators.atr import calculate_atr
