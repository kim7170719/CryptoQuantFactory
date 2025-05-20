import pandas as pd
from strategies.arbitrage.triangular import TriangularArbitrageStrategy

def test_triangular_arbitrage():
    data = pd.DataFrame({'pair1': [1]*30, 'pair2': [1]*30, 'pair3': [1]*30})
    strat = TriangularArbitrageStrategy()
    signals = strat.generate_signals(data)
    assert len(signals) == len(data)
