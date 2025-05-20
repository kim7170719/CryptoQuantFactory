import pandas as pd
import logging

class BacktestEngine:
    def __init__(self, strategy, data, initial_cash=10000, fee=0.001, slippage=0.0005, capital_management=None):
        self.strategy = strategy
        self.data = data.copy()
        self.initial_cash = initial_cash
        self.fee = fee
        self.slippage = slippage
        self.capital_management = capital_management
        self.results = None

    def run(self):
        try:
            signals = self.strategy.generate_signals(self.data)
            self.data['signal'] = signals
            self.data['position'] = self.data['signal'].shift(1).fillna(0)
            self.data['returns'] = self.data['close'].pct_change() * self.data['position']
            # 滑點與手續費
            self.data['returns'] -= self.fee
            self.data['returns'] -= self.slippage
            # 資金管理
            if self.capital_management:
                self.data['returns'] *= self.data['position'].apply(lambda x: self.capital_management.allocate(self.initial_cash, x)) / self.initial_cash
            self.data['equity'] = (1 + self.data['returns']).cumprod() * self.initial_cash
            self.results = self.data
            return self.data
        except Exception as e:
            logging.error(f'BacktestEngine run error: {e}')
            return pd.DataFrame()
