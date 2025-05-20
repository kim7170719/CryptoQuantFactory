from trading.paper_trading import PaperTrading

def test_paper_trading():
    pt = PaperTrading()
    pt.send_order(1, 100, 1)
    pt.send_order(-1, 110, 1)
    status = pt.get_status()
    assert 'cash' in status and 'position' in status
