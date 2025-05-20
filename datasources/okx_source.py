import requests
import pandas as pd
import logging

class OKXSource:
    def __init__(self, api_key=None, secret=None, passphrase=None):
        self.base_url = 'https://www.okx.com/api/v5/market/candles'
        # 實盤可用API Key等

    def fetch_ohlcv(self, symbol, timeframe='1D', limit=100):
        params = {'instId': symbol, 'bar': timeframe, 'limit': limit}
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if 'data' in data:
                df = pd.DataFrame(data['data'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                return df
            else:
                logging.error(f'OKX API error: {data}')
                return pd.DataFrame()
        except Exception as e:
            logging.error(f'Failed to fetch ohlcv from OKX: {e}')
            return pd.DataFrame()
