import requests
import pandas as pd
import logging

class BybitSource:
    def __init__(self, api_key=None, secret=None):
        self.base_url = 'https://api.bybit.com/v5/market/kline'
        # 實盤可用API Key等

    def fetch_ohlcv(self, symbol, interval='D', limit=100):
        params = {'symbol': symbol, 'interval': interval, 'limit': limit}
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if 'result' in data and 'list' in data['result']:
                df = pd.DataFrame(data['result']['list'], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                return df
            else:
                logging.error(f'Bybit API error: {data}')
                return pd.DataFrame()
        except Exception as e:
            logging.error(f'Failed to fetch ohlcv from Bybit: {e}')
            return pd.DataFrame()
