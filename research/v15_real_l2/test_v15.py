import unittest
import pandas as pd
from v15_btc_public_l2 import report_from_series
class TestV15(unittest.TestCase):
 def sample(self):
  idx=pd.date_range("2026-10-01",periods=86400,freq="s",tz="UTC")
  return pd.DataFrame({"mid":[80000.]*86400,"spread":[.1]*86400,"spread_bps":[.0125]*86400},index=idx)
 def test_real_book_metric_contract(self):
  r=report_from_series(self.sample(),{"canonical":{"events":123},"gaps":[]},"test")
  self.assertEqual(r["available_bbo_seconds"],86400)
  self.assertEqual(r["median_spread_bps"],.0125)
  self.assertEqual(r["pnl_status"],"NOT_CALCULATED_NO_MATCHED_TICK_TRADES")
 def test_gaps_are_not_filled(self):
  f=self.sample();f.iloc[:100,:]=float("nan")
  self.assertEqual(report_from_series(f,{},"test")["available_bbo_seconds"],86300)
 def test_invalid_spread_rejected(self):
  f=self.sample();f.iloc[1,f.columns.get_loc("spread")]=-1
  with self.assertRaises(ValueError):report_from_series(f,{},"test")
 def test_wrong_day_rejected(self):
  with self.assertRaises(ValueError):report_from_series(self.sample().iloc[:100],{},"test")
if __name__=="__main__":unittest.main()
