from strategies.base_strategy import BaseStrategy
import pandas as pd

class BollingerBandsStrategy(BaseStrategy):
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std

    def set_params(self, **params):
        self.window = params.get('window', self.window)
        self.num_std = params.get('num_std', self.num_std)

    def generate_signals(self, data):
        data['ma'] = data['close'].rolling(self.window).mean()
        data['std'] = data['close'].rolling(self.window).std()
        data['upper'] = data['ma'] + self.num_std * data['std']
        data['lower'] = data['ma'] - self.num_std * data['std']
        data['signal'] = 0
        data.loc[data['close'] > data['upper'], 'signal'] = -1
        data.loc[data['close'] < data['lower'], 'signal'] = 1
        return data['signal']
