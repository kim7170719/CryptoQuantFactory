import pandas as pd
from strategies.traditional.macd import MACDStrategy

def test_macd():
    data = pd.DataFrame({'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]})
    strat = MACDStrategy()
    signals = strat.generate_signals(data)
    assert len(signals) == len(data)
