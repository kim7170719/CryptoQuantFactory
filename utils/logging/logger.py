import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '../../logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y-%m-%d")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('CryptoQuantFactory')
