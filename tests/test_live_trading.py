from trading.live_trading import LiveTrading

def test_live_trading():
    class DummyAPI:
        def __init__(self):
            self.orders = []
        def send_order(self, *args, **kwargs):
            self.orders.append((args, kwargs))
        def get_status(self):
            return {'cash': 10000, 'position': 0}
    api = DummyAPI()
    lt = LiveTrading(api)
    lt.send_order(1, 100, 1)
    status = lt.get_status()
    assert 'cash' in status and 'position' in status
