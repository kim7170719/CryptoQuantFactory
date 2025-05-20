from strategies.base_strategy import BaseStrategy
import pandas as pd

class MACDStrategy(BaseStrategy):
    def __init__(self, fast=12, slow=26, signal=9):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def set_params(self, **params):
        self.fast = params.get('fast', self.fast)
        self.slow = params.get('slow', self.slow)
        self.signal = params.get('signal', self.signal)

    def generate_signals(self, data):
        data['ema_fast'] = data['close'].ewm(span=self.fast, adjust=False).mean()
        data['ema_slow'] = data['close'].ewm(span=self.slow, adjust=False).mean()
        data['macd'] = data['ema_fast'] - data['ema_slow']
        data['macd_signal'] = data['macd'].ewm(span=self.signal, adjust=False).mean()
        data['signal'] = 0
        data.loc[data['macd'] > data['macd_signal'], 'signal'] = 1
        data.loc[data['macd'] < data['macd_signal'], 'signal'] = -1
        return data['signal']
