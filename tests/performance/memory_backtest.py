import pandas as pd
from memory_profiler import profile
from backtest.engine import BacktestEngine
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

@profile
def run_backtest():
    data = pd.DataFrame({'close': [i for i in range(100000)]})
    strategy = MovingAverageCrossStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(strategy, data)
    results = engine.run()

if __name__ == '__main__':
    run_backtest()
