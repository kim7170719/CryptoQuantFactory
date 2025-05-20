import time
import pandas as pd
from backtest.engine import BacktestEngine
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

def test_backtest_performance():
    # 產生大數據量測試
    data = pd.DataFrame({'close': [i for i in range(100000)]})
    strategy = MovingAverageCrossStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(strategy, data)
    start = time.time()
    results = engine.run()
    duration = time.time() - start
    print(f'Backtest 100,000 rows duration: {duration:.2f}s')
    assert duration < 10  # 10秒內完成
