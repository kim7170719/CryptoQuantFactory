import pandas as pd
import logging

class MultiAssetBacktestEngine:
    def __init__(self, strategies, data_dict, initial_cash=10000, fee=0.001, slippage=0.0005, merge_equity=True):
        self.strategies = strategies  # dict: {symbol: strategy}
        self.data_dict = data_dict    # dict: {symbol: DataFrame}
        self.initial_cash = initial_cash
        self.fee = fee
        self.slippage = slippage
        self.merge_equity = merge_equity
        self.results = {}

    def run(self):
        try:
            for symbol, strategy in self.strategies.items():
                data = self.data_dict[symbol].copy()
                signals = strategy.generate_signals(data)
                data['signal'] = signals
                data['position'] = data['signal'].shift(1).fillna(0)
                data['returns'] = data['close'].pct_change() * data['position']
                data['returns'] -= self.fee
                data['returns'] -= self.slippage
                data['equity'] = (1 + data['returns']).cumprod() * (self.initial_cash / len(self.strategies))
                self.results[symbol] = data
            if self.merge_equity:
                merged = pd.DataFrame({k: v['equity'] for k, v in self.results.items()})
                merged['total_equity'] = merged.sum(axis=1)
                self.results['merged'] = merged
            return self.results
        except Exception as e:
            logging.error(f'MultiAssetBacktestEngine run error: {e}')
            return {}
