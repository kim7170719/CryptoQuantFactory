import pandas as pd
import json
import os
from backtest.engine import BacktestEngine
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

REGRESSION_FILE = 'tests/regression/ma_cross_regression.json'

def test_regression_backtest():
    data = pd.DataFrame({'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]})
    strategy = MovingAverageCrossStrategy(short_window=2, long_window=3)
    engine = BacktestEngine(strategy, data)
    results = engine.run()
    final_equity = float(results['equity'].iloc[-1])
    if not os.path.exists(REGRESSION_FILE):
        with open(REGRESSION_FILE, 'w') as f:
            json.dump({'final_equity': final_equity}, f)
    else:
        with open(REGRESSION_FILE) as f:
            baseline = json.load(f)
        assert abs(final_equity - baseline['final_equity']) < 1e-6
