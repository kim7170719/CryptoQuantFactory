from strategies.base_strategy import BaseStrategy

class SampleStrategyPlugin(BaseStrategy):
    def generate_signals(self, data):
        data['signal'] = 1  # always long for demo
        return data['signal']
    def set_params(self, **params):
        pass
