import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from v17_maker_proxy import at,tickround,test_strategy
class TestV17(unittest.TestCase):
 def sample(self):
  t=list(range(1000000,18000000,500000))
  return {"times":t,"bids":[100.0]*len(t),"asks":[100.1]*len(t)}
 def tr(self,p=99.8,side="sell"):
  return [{"local_timestamp":str(t),"side":side,"price":str(p),"amount":"2"} for t in range(3000000,16000000,500000)]
 def test_time_no_lookahead(self):
  b=self.sample()
  self.assertIsNone(at(b,1000000))
  self.assertEqual(at(b,1500000)[0],100)
 def test_tick(self):
  self.assertAlmostEqual(tickround(100.15,.1,True),100.1)
  self.assertAlmostEqual(tickround(100.15,.1,False),100.2)
 def test_no_fill_on_touch(self):
  self.assertEqual(test_strategy(self.sample(),self.tr(100),"BTCUSDT","top")["maker_fills"],0)
 def test_trade_through_and_cost(self):
  r=test_strategy(self.sample(),self.tr(),"BTCUSDT","top")
  self.assertGreater(r["maker_fills"],0)
  self.assertLess(r["pnl_usdt"],0)
  self.assertGreater(r["fees_usdt"],0)
 def test_wider_quotes_no_more_fills(self):
  a=test_strategy(self.sample(),self.tr(),"BTCUSDT","top")
  b=test_strategy(self.sample(),self.tr(),"BTCUSDT","wide_5bp")
  self.assertGreaterEqual(a["maker_fills"],b["maker_fills"])
if __name__=="__main__":unittest.main()
