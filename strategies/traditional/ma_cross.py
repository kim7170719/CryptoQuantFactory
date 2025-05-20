from strategies.base_strategy import BaseStrategy
import pandas as pd

class MovingAverageCrossStrategy(BaseStrategy):
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def set_params(self, **params):
        self.short_window = params.get('short_window', self.short_window)
        self.long_window = params.get('long_window', self.long_window)

    def generate_signals(self, data):
        data['short_ma'] = data['close'].rolling(self.short_window).mean()
        data['long_ma'] = data['close'].rolling(self.long_window).mean()
        data['signal'] = 0
        data.loc[data['short_ma'] > data['long_ma'], 'signal'] = 1
        data.loc[data['short_ma'] < data['long_ma'], 'signal'] = -1
        return data['signal']
