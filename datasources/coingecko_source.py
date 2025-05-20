import requests
import pandas as pd
import logging

class CoinGeckoSource:
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3/'

    def fetch_ohlcv(self, coin_id, vs_currency='usd', days='max'):
        url = f"{self.base_url}coins/{coin_id}/market_chart"
        params = {'vs_currency': vs_currency, 'days': days}
        try:
            response = requests.get(url, params=params)
            data = response.json()
            if 'prices' in data:
                prices = data['prices']
                df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                return df
            else:
                logging.error(f'CoinGecko API error: {data}')
                return pd.DataFrame()
        except Exception as e:
            logging.error(f'Failed to fetch ohlcv from CoinGecko: {e}')
            return pd.DataFrame()
