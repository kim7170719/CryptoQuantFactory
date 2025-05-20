from strategies.base_strategy import BaseStrategy
import numpy as np

class DummyDQNModel:
    def predict(self, data):
        # 假設有訓練好的模型，這裡僅示範
        return np.random.choice([-1, 0, 1], size=len(data))

class DQNStrategy(BaseStrategy):
    def __init__(self, model=None):
        self.model = model or DummyDQNModel()

    def set_params(self, **params):
        self.model = params.get('model', self.model)

    def generate_signals(self, data):
        return self.model.predict(data)
