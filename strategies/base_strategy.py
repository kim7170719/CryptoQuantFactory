from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, data):
        pass

    @abstractmethod
    def set_params(self, **params):
        pass
