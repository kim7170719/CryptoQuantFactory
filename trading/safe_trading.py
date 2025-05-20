from trading.paper_trading import PaperTrading
from trading.live_trading import LiveTrading
import logging

class SafeTrading:
    def __init__(self, mode='paper', api=None, risk_control=None):
        self.mode = mode
        self.risk_control = risk_control
        if mode == 'paper':
            self.trader = PaperTrading()
        else:
            self.trader = LiveTrading(api)

    def send_order(self, signal, price, size, account):
        try:
            if self.risk_control:
                ok, msg = self.risk_control.check_order({'size': size}, account)
                if not ok:
                    return {'status': 'rejected', 'reason': msg}
            self.trader.send_order(signal, price, size)
            return {'status': 'success'}
        except Exception as e:
            logging.error(f'SafeTrading send_order error: {e}')
            return {'status': 'error', 'reason': str(e)}

    def get_status(self):
        return self.trader.get_status()
