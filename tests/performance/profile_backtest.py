import cProfile
import pandas as pd
from backtest.engine import BacktestEngine
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

data = pd.DataFrame({'close': [i for i in range(100000)]})
strategy = MovingAverageCrossStrategy(short_window=20, long_window=50)
engine = BacktestEngine(strategy, data)
cProfile.run('engine.run()', 'backtest_profile.prof')
print('Profile saved to backtest_profile.prof')
