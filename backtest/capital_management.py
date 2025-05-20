class CapitalManagement:
    def __init__(self, max_leverage=1, mode='fixed'):
        self.max_leverage = max_leverage
        self.mode = mode
    def allocate(self, equity, signal):
        if self.mode == 'fixed':
            return equity * self.max_leverage * abs(signal)
        elif self.mode == 'percent':
            return equity * self.max_leverage * 0.1 * abs(signal)
        else:
            return equity * abs(signal)
