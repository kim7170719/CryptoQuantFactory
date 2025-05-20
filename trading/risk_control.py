class RiskControl:
    def __init__(self, max_loss_per_trade=0.02, max_daily_loss=0.1, max_position=1.0):
        self.max_loss_per_trade = max_loss_per_trade
        self.max_daily_loss = max_daily_loss
        self.max_position = max_position
        self.daily_loss = 0

    def check_order(self, order, account):
        if abs(order['size']) > self.max_position * account['equity']:
            return False, 'Position size exceeds limit.'
        return True, ''

    def update_daily_loss(self, loss):
        self.daily_loss += loss
        if self.daily_loss > self.max_daily_loss:
            return False, 'Daily loss limit exceeded.'
        return True, ''
