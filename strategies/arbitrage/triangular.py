from strategies.base_strategy import BaseStrategy
import pandas as pd

class TriangularArbitrageStrategy(BaseStrategy):
    def __init__(self, threshold=0.001):
        self.threshold = threshold

    def set_params(self, **params):
        self.threshold = params.get('threshold', self.threshold)

    def generate_signals(self, data):
        # 假設data包含三個幣對的價格：pair1, pair2, pair3
        # 三角套利公式：pair1 * pair2 / pair3 - 1
        data['spread'] = data['pair1'] * data['pair2'] / data['pair3'] - 1
        data['signal'] = 0
        data.loc[data['spread'] > self.threshold, 'signal'] = 1
        data.loc[data['spread'] < -self.threshold, 'signal'] = -1
        return data['signal']
