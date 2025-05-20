from strategies.base_strategy import BaseStrategy
import pandas as pd

class CalendarArbitrageStrategy(BaseStrategy):
    def __init__(self, threshold=0.001):
        self.threshold = threshold

    def set_params(self, **params):
        self.threshold = params.get('threshold', self.threshold)

    def generate_signals(self, data):
        # 假設data包含近月與遠月合約價格：near, far
        data['spread'] = data['near'] - data['far']
        data['signal'] = 0
        data.loc[data['spread'] > self.threshold, 'signal'] = -1
        data.loc[data['spread'] < -self.threshold, 'signal'] = 1
        return data['signal']
