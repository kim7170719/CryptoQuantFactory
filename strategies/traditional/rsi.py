from strategies.base_strategy import BaseStrategy
import pandas as pd

class RSIStrategy(BaseStrategy):
    def __init__(self, period=14, overbought=70, oversold=30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def set_params(self, **params):
        self.period = params.get('period', self.period)
        self.overbought = params.get('overbought', self.overbought)
        self.oversold = params.get('oversold', self.oversold)

    def generate_signals(self, data):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        data['rsi'] = rsi
        data['signal'] = 0
        data.loc[data['rsi'] > self.overbought, 'signal'] = -1
        data.loc[data['rsi'] < self.oversold, 'signal'] = 1
        return data['signal']
