from strategies.base_strategy import BaseStrategy

class RLStrategy(BaseStrategy):
    def __init__(self, model=None):
        self.model = model

    def set_params(self, **params):
        self.model = params.get('model', self.model)

    def generate_signals(self, data):
        # 假設model已訓練好，並有predict方法
        if self.model:
            return self.model.predict(data)
        else:
            return [0] * len(data)
