from strategies.base_strategy import BaseStrategy

class ArbitrageStrategy(BaseStrategy):
    def __init__(self, threshold=0.01):
        self.threshold = threshold

    def set_params(self, **params):
        self.threshold = params.get('threshold', self.threshold)

    def generate_signals(self, data):
        # 假設data包含多交易所價格
        data['spread'] = data['exchange1'] - data['exchange2']
        data['signal'] = 0
        data.loc[data['spread'] > self.threshold, 'signal'] = -1  # 賣出exchange1，買入exchange2
        data.loc[data['spread'] < -self.threshold, 'signal'] = 1  # 買入exchange1，賣出exchange2
        return data['signal']
