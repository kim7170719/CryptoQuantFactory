import random

class SlippageModel:
    def __init__(self, slippage=0.0005, randomize=False):
        self.slippage = slippage
        self.randomize = randomize
    def apply(self, price):
        if self.randomize:
            return price * (1 + random.uniform(-self.slippage, self.slippage))
        return price * (1 + self.slippage)
