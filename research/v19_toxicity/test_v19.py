import unittest
from v19_toxicity_oos import reconstruct,quotes,score,permitted,RULES
def r(t,side,price,amount,snapshot):
 return {"local_timestamp":str(t),"is_snapshot":str(snapshot).lower(),"side":side,"price":str(price),"amount":str(amount)}
class TestV19(unittest.TestCase):
 def book(self):
  a=[r(1_000_000,"bid",100,5,True),r(1_000_000,"ask",100.1,3,True)]
  for i in range(2,52):a.append(r(i*1_000_000,"bid",100,5,False))
  return reconstruct(a)[0]
 def tape(self,px):
  return [{"local_timestamp":str(i*1000000+500000),"side":"sell","price":str(px),"amount":"5"} for i in range(2,47)]
 def test_complete_snapshot(self):self.assertGreater(len(self.book()),10)
 def test_one_sided_fails(self):
  with self.assertRaises(ValueError):reconstruct([r(1,"bid",100,1,True),r(2,"bid",100,1,False)])
 def test_crossed_fails(self):
  with self.assertRaises(ValueError):reconstruct([r(1,"bid",101,1,True),r(1,"ask",100,1,True),r(2,"bid",101,1,False)])
 def test_non_crossing(self):self.assertEqual(quotes(self.book(),self.tape(100),"BTCUSDT")[0],[])
 def test_crossing(self):
  a,_=quotes(self.book(),self.tape(99.8),"BTCUSDT")
  self.assertTrue(a)
  self.assertAlmostEqual(a[0]["net_bps"],a[0]["gross_bps"]-7)
 def test_no_duplicate_cycles(self):
  a,_=quotes(self.book(),self.tape(99.8),"BTCUSDT")
  self.assertEqual(score(a,"all")["fills"],len(set(e["qtime"] for e in a)))
 def test_filter(self):
  self.assertFalse(permitted({"imb":-1,"micro":0,"flow":0},"imb0"))
  self.assertEqual(len(RULES),8)
 def test_empty(self):self.assertEqual(score([],"all")["pnl_usdt"],0)
if __name__=="__main__":unittest.main()
