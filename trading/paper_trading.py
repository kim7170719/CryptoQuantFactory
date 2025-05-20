import logging

class PaperTrading:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0
        self.history = []
    def send_order(self, signal, price, size):
        try:
            self.position += signal * size
            self.cash -= signal * size * price
            self.history.append({'signal': signal, 'price': price, 'size': size, 'cash': self.cash, 'position': self.position})
        except Exception as e:
            logging.error(f'PaperTrading send_order error: {e}')
    def get_status(self):
        return {'cash': self.cash, 'position': self.position}
