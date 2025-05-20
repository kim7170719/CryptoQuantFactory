from itertools import product
import logging

class GridSearchOptimizer:
    def __init__(self, strategy_class, data, param_grid):
        self.strategy_class = strategy_class
        self.data = data
        self.param_grid = param_grid

    def optimize(self):
        keys, values = zip(*self.param_grid.items())
        best_score = float('-inf')
        best_params = None
        for v in product(*values):
            params = dict(zip(keys, v))
            try:
                strategy = self.strategy_class(**params)
                signals = strategy.generate_signals(self.data)
                returns = self.data['close'].pct_change() * signals.shift(1).fillna(0)
                score = returns.sum()
                if score > best_score:
                    best_score = score
                    best_params = params
            except Exception as e:
                logging.error(f'GridSearchOptimizer error: {e}')
        return best_params
