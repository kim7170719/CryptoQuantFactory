from strategies.base_strategy import BaseStrategy
import pandas as pd

class MomentumValueStrategy(BaseStrategy):
    def __init__(self, momentum_window=10, value_window=252, value_threshold=0):
        self.momentum_window = momentum_window
        self.value_window = value_window
        self.value_threshold = value_threshold

    def set_params(self, **params):
        self.momentum_window = params.get('momentum_window', self.momentum_window)
        self.value_window = params.get('value_window', self.value_window)
        self.value_threshold = params.get('value_threshold', self.value_threshold)

    def generate_signals(self, data):
        data['momentum'] = data['close'].pct_change(self.momentum_window)
        data['value'] = data['close'] / data['close'].rolling(self.value_window).max()
        data['score'] = data['momentum'] + data['value']
        data['signal'] = data['score'].apply(lambda x: 1 if x > self.value_threshold else -1)
        return data['signal']
