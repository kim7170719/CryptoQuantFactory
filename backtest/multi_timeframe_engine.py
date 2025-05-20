import pandas as pd
import logging

class MultiTimeframeBacktestEngine:
    def __init__(self, strategy, data_dict, initial_cash=10000, fee=0.001, slippage=0.0005):
        self.strategy = strategy
        self.data_dict = data_dict  # dict: {timeframe: DataFrame}
        self.initial_cash = initial_cash
        self.fee = fee
        self.slippage = slippage
        self.results = None

    def run(self):
        try:
            # 假設策略能處理多時間框架
            signals = self.strategy.generate_signals(self.data_dict)
            main_data = self.data_dict['main'].copy()
            main_data['signal'] = signals
            main_data['position'] = main_data['signal'].shift(1).fillna(0)
            main_data['returns'] = main_data['close'].pct_change() * main_data['position']
            main_data['returns'] -= self.fee
            main_data['returns'] -= self.slippage
            main_data['equity'] = (1 + main_data['returns']).cumprod() * self.initial_cash
            self.results = main_data
            return main_data
        except Exception as e:
            logging.error(f'MultiTimeframeBacktestEngine run error: {e}')
            return pd.DataFrame()
