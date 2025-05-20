import optuna
import logging

class StrategyOptimizer:
    def __init__(self, strategy_class, data, param_space, n_trials=50):
        self.strategy_class = strategy_class
        self.data = data
        self.param_space = param_space
        self.n_trials = n_trials

    def objective(self, trial):
        try:
            params = {k: trial.suggest_float(k, *v) for k, v in self.param_space.items()}
            strategy = self.strategy_class(**params)
            signals = strategy.generate_signals(self.data)
            returns = self.data['close'].pct_change() * signals.shift(1).fillna(0)
            return returns.sum()
        except Exception as e:
            logging.error(f'Optimizer objective error: {e}')
            return -1e9

    def optimize(self):
        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=self.n_trials)
        return study.best_params
