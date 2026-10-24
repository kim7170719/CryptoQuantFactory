#!/usr/bin/env python3
"""CandleFeed 2026-10-01 BTCUSDT REAL Binance USD-M L2 public book audit.
NO fabricated fills or PnL. NEVER publish raw files (internal-use only).
"""
import argparse, hashlib, json
from pathlib import Path
SYMBOL="BTCUSDT";DAY="2026-10-01"
def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(4*1024*1024),b""):h.update(c)
    return h.hexdigest()
def report_from_series(series, manifest, sha):
    if not {"mid","spread_bps","spread"}.issubset(series.columns):raise ValueError("UNEXPECTED_SPREAD_COLUMNS")
    if len(series)!=86400:raise ValueError("EXPECTED_86400_SECONDS")
    good=series.dropna(subset=["mid","spread_bps","spread"])
    if good.empty:raise ValueError("NO_VALID_BBO")
    if (good["spread"]<=0).any() or (good["mid"]<=0).any():raise ValueError("CROSSED_OR_INVALID_BBO")
    hourly=[]
    for h,g in series.groupby(series.index.hour):
        ok=g.dropna(subset=["mid","spread_bps","spread"])
        hourly.append({"hour_utc":int(h),"available_s":len(ok),"total_s":len(g),"median_spread_bps":round(float(ok["spread_bps"].median()),8) if len(ok) else None})
    can=manifest.get("canonical",{})
    med=float(good["spread_bps"].median())
    return {"data_origin":"CandleFeed third-party capture of Binance USD-M","symbol":SYMBOL,"day":DAY,
      "manifest_sha256":sha,"depth_events":can.get("events"),"segments":can.get("segments"),
      "recorded_gaps":len(manifest.get("gaps",[])),
      "available_bbo_seconds":len(good),"total_seconds":len(series),"bbo_coverage_pct":round(len(good)/864,5),
      "median_spread_bps":round(med,8),"p99_spread_bps":round(float(good["spread_bps"].quantile(.99)),8),
      "fraction_one_tick_or_less":round(float((good["spread"]<=.100001).mean()),7),
      "assumed_maker_bps_each_fill":2,"two_maker_fee_bps":4,"median_spread_div_4bps":round(med/4,8),
      "hourly":hourly,"pnl_status":"NOT_CALCULATED_NO_MATCHED_TICK_TRADES",
      "limitations":["Raw L2 files internal-use only; never redistribute",
         "No market-order trade tape in public no-key book sample",
         "Not a FIFO fill or profitability study","BBO unknown outside anchor window",
         "Assumed maker fee not verified with any account"]}
def run(out,data):
    from candlefeed import CandleFeed
    from candlefeed.l2book import L2Book
    api=CandleFeed(public=True)
    got=api.download_l2_sample(SYMBOL,DAY,str(data))
    folder=data/"book"/"binance"/SYMBOL/DAY
    manifest_path=folder/"manifest.json"
    if not manifest_path.is_file():raise FileNotFoundError("SAMPLE_MANIFEST_MISSING")
    manifest=json.loads(manifest_path.read_text())
    book=L2Book.load(data,SYMBOL,DAY)
    one_sec=book.spread_series("1s")
    report=report_from_series(one_sec,manifest,digest(manifest_path))
    report["files_downloaded"]=len(got.get("downloaded",[]))
    report["bytes_fetched"]=got.get("bytes")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"bbo_coverage_pct":report["bbo_coverage_pct"],"median_spread_bps":report["median_spread_bps"],"pnl_status":report["pnl_status"]},indent=2))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,default=Path("v15_book_report.json"))
    p.add_argument("--data",type=Path,default=Path("l2_sample_data"))
    a=p.parse_args()
    try:run(a.out,a.data)
    except Exception as e:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps({"status":"FAILED","type":type(e).__name__,"error":str(e)},indent=2)+"\n")
        raise
if __name__=="__main__":main()
