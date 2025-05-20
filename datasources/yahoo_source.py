import yfinance as yf
import pandas as pd
import logging

class YahooSource:
    def fetch_ohlcv(self, symbol, start=None, end=None, interval='1d'):
        try:
            data = yf.download(symbol, start=start, end=end, interval=interval)
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            logging.error(f'Failed to fetch ohlcv from Yahoo for {symbol}: {e}')
            return pd.DataFrame()
