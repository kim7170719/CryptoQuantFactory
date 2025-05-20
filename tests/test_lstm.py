import pandas as pd
import numpy as np
from strategies.rl_dl.lstm import LSTMStrategy

def test_lstm():
    data = pd.DataFrame({'close': np.arange(1, 31)})
    strat = LSTMStrategy()
    signals = strat.generate_signals(data)
    assert len(signals) == len(data)
