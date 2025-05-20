import pandas as pd
from backtest.multi_timeframe_engine import MultiTimeframeBacktestEngine
from strategies.traditional.rsi import RSIStrategy

def test_multi_timeframe():
    main = pd.DataFrame({'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]})
    aux = pd.DataFrame({'close': [2,3,4,5,6,5,4,3,2,3,4,5,6,7,8,9,10,11,10,9,8,7,6,5,4,3,2]})
    data_dict = {'main': main, 'aux': aux}
    strat = RSIStrategy()
    engine = MultiTimeframeBacktestEngine(strat, data_dict)
    results = engine.run()
    assert 'equity' in results
