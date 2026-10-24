import unittest
from v18_inventory_netting import simulate,config_set
def bbo(n=100):
 t=[i*500000 for i in range(2,n+2)]
 return {"times":t,"bids":[100.0]*len(t),"asks":[100.1]*len(t),"bad_bbo":0}
def tape(price=99.8,side="sell"):
 return [{"local_timestamp":str(t),"side":side,"price":str(price),"amount":"4"} for t in range(3000000,38000000,500000)]
class TestV18(unittest.TestCase):
 def cfg(self,hold=15,mode="none",width=0):
  return {"width_bps":width,"hold_s":hold,"flow_mode":mode}
 def test_conservative_hedge_cash(self):
  r=simulate(bbo(),tape(),"BTCUSDT",self.cfg(1))
  self.assertTrue(r["zero_delta_at_end"])
  self.assertGreater(r["entries"],0)
  self.assertGreater(r["taker_exits"],0)
  self.assertGreater(r["fee_usdt"],0)
 def test_maker_to_maker_pairs(self):
  a=tape()[:18];b=tape(100.3,"buy")[18:];z=sorted(a+b,key=lambda x:int(x["local_timestamp"]))
  r=simulate(bbo(),z,"BTCUSDT",self.cfg(30))
  self.assertTrue(r["zero_delta_at_end"])
  self.assertGreater(r["maker_exits"],0)
 def test_no_fill_on_touch(self):
  r=simulate(bbo(),tape(100.0),"BTCUSDT",self.cfg())
  self.assertEqual(r["entries"],0)
  self.assertEqual(r["pnl_usdt"],0)
 def test_fee_consistency(self):
  r=simulate(bbo(),tape(),"BTCUSDT",self.cfg(1))
  self.assertAlmostEqual(r["pnl_usdt"]+r["fee_usdt"],r["gross_before_all_fees_usdt"],places=4)
 def test_config_grid(self):
  self.assertEqual(len(config_set()),60)
 def test_bad_book_rejected(self):
  x=bbo();x["bad_bbo"]=1
  with self.assertRaises(ValueError):simulate(x,tape(),"BTCUSDT",self.cfg())
if __name__=="__main__":unittest.main()
