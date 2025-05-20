from strategies.base_strategy import BaseStrategy
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class LSTMStrategy(BaseStrategy):
    def __init__(self, model=None, window=10):
        self.model = model or self._build_model()
        self.window = window

    def _build_model(self):
        model = Sequential([
            LSTM(32, input_shape=(self.window, 1)),
            Dense(1, activation='tanh')
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def set_params(self, **params):
        self.window = params.get('window', self.window)

    def generate_signals(self, data):
        # 僅示範：實際應先訓練模型
        if len(data) < self.window:
            return [0] * len(data)
        X = np.array(data['close'].tail(self.window)).reshape(1, self.window, 1)
        pred = self.model.predict(X)[0, 0]
        return [1 if pred > 0 else -1] * len(data)
