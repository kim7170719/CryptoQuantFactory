import pandas as pd
from backtest.multi_asset_engine import MultiAssetBacktestEngine
from strategies.traditional.rsi import RSIStrategy

def test_multi_asset():
    data1 = pd.DataFrame({'close': [1,2,3,4,5,4,3,2,1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]})
    data2 = pd.DataFrame({'close': [2,3,4,5,6,5,4,3,2,3,4,5,6,7,8,9,10,11,10,9,8,7,6,5,4,3,2]})
    strategies = {'BTC': RSIStrategy(), 'ETH': RSIStrategy()}
    data_dict = {'BTC': data1, 'ETH': data2}
    engine = MultiAssetBacktestEngine(strategies, data_dict)
    results = engine.run()
    assert 'BTC' in results and 'ETH' in results
