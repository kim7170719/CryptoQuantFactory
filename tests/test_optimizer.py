import pandas as pd
from optimizer.optimizer import StrategyOptimizer
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

def test_optimizer():
    data = pd.DataFrame({
        'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
    })
    param_space = {'short_window': (2, 5), 'long_window': (3, 10)}
    optimizer = StrategyOptimizer(MovingAverageCrossStrategy, data, param_space, n_trials=2)
    best_params = optimizer.optimize()
    assert 'short_window' in best_params
    assert 'long_window' in best_params
