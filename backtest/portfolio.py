import pandas as pd
import logging

class Portfolio:
    def __init__(self, strategies, weights):
        self.strategies = strategies
        self.weights = weights

    def combine_signals(self, data):
        try:
            combined = pd.DataFrame(index=data.index)
            for strat, w in zip(self.strategies, self.weights):
                combined[strat.__class__.__name__] = strat.generate_signals(data) * w
            combined['signal'] = combined.sum(axis=1)
            return combined['signal']
        except Exception as e:
            logging.error(f'Portfolio combine_signals error: {e}')
            return pd.Series([0]*len(data), index=data.index)
