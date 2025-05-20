import ccxt
import pandas as pd
import logging

class CCXTSource:
    def __init__(self, exchange_name='binance'):
        try:
            self.exchange = getattr(ccxt, exchange_name)()
        except Exception as e:
            logging.error(f'Failed to init exchange {exchange_name}: {e}')
            raise

    def fetch_ohlcv(self, symbol, timeframe='1d', since=None, limit=1000):
        try:
            data = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logging.error(f'Failed to fetch ohlcv for {symbol} on {self.exchange.id}: {e}')
            return pd.DataFrame()
