import pandas as pd
from strategies.rl_dl.dqn import DQNStrategy

def test_dqn():
    data = pd.DataFrame({'close': [1]*30})
    strat = DQNStrategy()
    signals = strat.generate_signals(data)
    assert len(signals) == len(data)
