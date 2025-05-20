import pandas as pd
from backtest.portfolio import Portfolio
from strategies.traditional.ma_cross import MovingAverageCrossStrategy

def test_portfolio():
    data = pd.DataFrame({
        'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
    })
    strat1 = MovingAverageCrossStrategy(short_window=2, long_window=3)
    strat2 = MovingAverageCrossStrategy(short_window=3, long_window=5)
    portfolio = Portfolio([strat1, strat2], [0.5, 0.5])
    signals = portfolio.combine_signals(data)
    assert len(signals) == len(data)
