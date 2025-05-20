from strategies.base_strategy import BaseStrategy
import pandas as pd

class MultiFactorStrategy(BaseStrategy):
    def __init__(self, factors=None):
        self.factors = factors or []

    def set_params(self, **params):
        self.factors = params.get('factors', self.factors)

    def generate_signals(self, data):
        score = pd.Series(0, index=data.index)
        for factor in self.factors:
            score += factor(data)
        data['signal'] = score.apply(lambda x: 1 if x > 0 else -1)
        return data['signal']
