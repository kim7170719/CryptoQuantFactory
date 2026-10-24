import unittest
from v16_tardis_first_minute import book_series,tape_join
class TestV16(unittest.TestCase):
 def setUp(self):
  self.rows=[{"local_timestamp":"1000000","is_snapshot":"true","side":"bid","price":"100","amount":"1"},
             {"local_timestamp":"1000000","is_snapshot":"true","side":"ask","price":"100.1","amount":"1"},
             {"local_timestamp":"2000000","is_snapshot":"false","side":"bid","price":"100.05","amount":"1"},
             {"local_timestamp":"3000000","is_snapshot":"false","side":"ask","price":"100.1","amount":"0"},
             {"local_timestamp":"3000000","is_snapshot":"false","side":"ask","price":"100.2","amount":"2"}]
 def test_bbo(self):
  r=book_series(self.rows)
  self.assertEqual(len(r["spread"]),2)
  self.assertEqual(r["bids"][-1],100.05)
  self.assertEqual(r["asks"][-1],100.2)
 def test_no_snapshot(self):
  self.assertEqual(book_series(self.rows[2:])["spread"],[])
 def test_no_lookahead(self):
  s=book_series(self.rows)
  z=tape_join(s,[{"local_timestamp":"1500000","side":"buy","price":"100.1","amount":"1"}])
  self.assertEqual(z["trades_matched_to_prior_bbo_within_1s"],0)
 def test_time_matched_sell(self):
  s=book_series(self.rows)
  z=tape_join(s,[{"local_timestamp":"2100000","side":"sell","price":"100.05","amount":"1"}])
  self.assertEqual(z["trades_at_or_beyond_opposite_bbo"],1)
if __name__=="__main__":unittest.main()
