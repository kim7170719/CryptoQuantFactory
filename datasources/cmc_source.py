import requests
import pandas as pd
import logging

class CMCSource:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://pro-api.coinmarketcap.com/v1/'

    def fetch_ohlcv(self, symbol, convert='USD', time_start=None, time_end=None):
        url = f"{self.base_url}cryptocurrency/ohlcv/historical"
        headers = {'X-CMC_PRO_API_KEY': self.api_key}
        params = {'symbol': symbol, 'convert': convert}
        if time_start:
            params['time_start'] = time_start
        if time_end:
            params['time_end'] = time_end
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            if 'data' in data and 'quotes' in data['data']:
                df = pd.DataFrame(data['data']['quotes'])
                df['timestamp'] = pd.to_datetime(df['time_open'])
                return df
            else:
                logging.error(f'CMC API error: {data}')
                return pd.DataFrame()
        except Exception as e:
            logging.error(f'Failed to fetch ohlcv from CMC: {e}')
            return pd.DataFrame()
