import logging

class LiveTrading:
    def __init__(self, api):
        self.api = api
    def send_order(self, signal, price, size):
        try:
            # 實盤下單接口，需根據api實現
            self.api.send_order(signal, price, size)
        except Exception as e:
            logging.error(f'LiveTrading send_order error: {e}')
    def get_status(self):
        try:
            return self.api.get_status()
        except Exception as e:
            logging.error(f'LiveTrading get_status error: {e}')
            return {}
