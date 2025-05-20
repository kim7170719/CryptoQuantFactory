import pandas as pd
from backtest.engine import BacktestEngine
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

def test_backtest_engine():
    data = pd.DataFrame({
        'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
    })
    strategy = MovingAverageCrossStrategy(short_window=2, long_window=3)
    engine = BacktestEngine(strategy, data)
    results = engine.run()
    assert 'equity' in results
    assert results['equity'].iloc[-1] > 0
