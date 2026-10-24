#!/usr/bin/env python3
"""Tardis free first-of-month genuine Binance Futures BTC/ETH book + trades audit.
Streams just 90 seconds. Raw events NEVER written to disk or shared.
Marketable-trade-vs-BBO is descriptive only, NOT simulated user Maker fills.
"""
import argparse,bisect,csv,datetime as dt,gzip,io,json,statistics
from collections import Counter
from pathlib import Path
import requests
VENUE="binance-futures"
URL="https://datasets.tardis.dev/v1/{}/{}/{}/{:02d}/01/{}.csv.gz"
def fetch(symbol,day,kind,seconds=90):
    date=dt.date.fromisoformat(day)
    if date.day!=1:raise ValueError("NO_KEY_SAMPLE_REQUIRES_FIRST_DAY")
    url=URL.format(VENUE,kind,date.year,date.month,symbol)
    with requests.get(url,stream=True,timeout=(20,45),headers={"Accept-Encoding":"identity"}) as resp:
        resp.raise_for_status()
        resp.raw.decode_content=False
        with gzip.GzipFile(fileobj=resp.raw) as gz:
            reader=csv.DictReader(io.TextIOWrapper(gz,encoding="utf-8",newline=""))
            needed={"exchange","symbol","timestamp","local_timestamp","side","price","amount"}
            if kind=="incremental_book_L2":needed.add("is_snapshot")
            if not needed.issubset(set(reader.fieldnames or [])):
                raise ValueError("UNKNOWN_SCHEMA:"+str(reader.fieldnames))
            start=None;last=None;rows=[]
            for row in reader:
                ts=int(row["local_timestamp"])
                if start is None:start=ts
                if ts-start>seconds*1_000_000:break
                if last is not None and ts<last:raise ValueError("LOCAL_TIME_REVERSED")
                if row["exchange"]!=VENUE or row["symbol"]!=symbol:raise ValueError("WRONG_MARKET")
                last=ts;rows.append(row)
                if len(rows)>=400000:raise ValueError("MAX_ROWS_CAP")
    if not rows:raise ValueError("EMPTY_FILE")
    return rows,url
def book_series(rows):
    bid={};ask={};snap_before=False;ready=False;times=[];bids=[];asks=[];spread=[];bad=0;snaps=0
    def mark(ts):
        nonlocal bad
        if not ready:return
        if not bid or not ask:bad+=1;return
        b=max(bid);a=min(ask)
        if a<=b:bad+=1;return
        times.append(ts);bids.append(b);asks.append(a);spread.append(1e4*(a-b)/((a+b)/2))
    prev_t=None;prev_snap=None
    for r in rows:
        ts=int(r["local_timestamp"]);snap=r["is_snapshot"].lower()=="true"
        if prev_t is not None and ts!=prev_t and prev_snap is not True:mark(prev_t)
        if snap and prev_snap is not True:
            bid={};ask={};ready=False;snaps+=1
        if not snap and prev_snap is True:ready=True
        side=r["side"].lower()
        if side not in ("bid","ask"):raise ValueError("BAD_SIDE")
        p=float(r["price"]);q=float(r["amount"])
        if p<=0 or q<0:raise ValueError("BAD_DEPTH")
        d=bid if side=="bid" else ask
        if q==0:d.pop(p,None)
        else:d[p]=q
        prev_snap=snap;prev_t=ts
    if prev_t is not None and prev_snap is not True:mark(prev_t)
    return {"times":times,"bids":bids,"asks":asks,"spread":spread,"snapshots":snaps,"bad_bbo":bad}
def tape_join(book,rows):
    ts=book["times"];matched=0;through=0;count=Counter();size=[]
    for r in rows:
        side=r["side"].lower()
        if side not in ("buy","sell"):continue
        count[side]+=1
        tt=int(r["local_timestamp"]);i=bisect.bisect_right(ts,tt)-1
        if i<0 or tt-ts[i]>1_000_000:continue
        matched+=1;p=float(r["price"]);q=float(r["amount"])
        through+=(p>=book["asks"][i] if side=="buy" else p<=book["bids"][i])
        size.append(p*q)
    return {"trade_rows":len(rows),"buy_aggressors":count["buy"],"sell_aggressors":count["sell"],
            "trades_matched_to_prior_bbo_within_1s":matched,
            "trades_at_or_beyond_opposite_bbo":through,
            "pct_opposite_bbo":round(100*through/matched,3) if matched else None,
            "median_matched_trade_notional":round(statistics.median(size),2) if size else None}
def analyze(symbol,day,seconds):
    ob,ob_url=fetch(symbol,day,"incremental_book_L2",seconds)
    tape,tape_url=fetch(symbol,day,"trades",seconds)
    bs=book_series(ob)
    if not bs["spread"]:raise ValueError("NO_COMPLETE_SNAPSHOT_PLUS_CONTINUOUS_BBO")
    return {"venue":VENUE,"symbol":symbol,"day":day,"sample_seconds_requested":seconds,
            "l2_rows":len(ob),"snapshot_count":bs["snapshots"],"bbo_event_groups":len(bs["spread"]),
            "invalid_bbo_event_groups":bs["bad_bbo"],
            "median_spread_bps":round(statistics.median(bs["spread"]),7),
            "p95_spread_bps":round(sorted(bs["spread"])[min(len(bs["spread"])-1,int(.95*len(bs["spread"])))],7),
            "trade_alignment":tape_join(bs,tape),
            "original_l2_url":ob_url,"original_trade_url":tape_url,
            "limitations":["Only a bounded first-window, not a complete day",
              "No exchange U/u sequence fields in normalized Tardis CSV",
              "Prior-book matched historical taker events are not the user's confirmed Maker fills",
              "No fee-adjusted strategy PnL or confidence interval from this sample"]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--day",default="2025-08-01");p.add_argument("--seconds",type=int,default=90)
    p.add_argument("--out",type=Path,default=Path("v16_real_ticks.json"));a=p.parse_args()
    result={"day":a.day,"status":"SUCCESS","assets":{}}
    for sym in ["BTCUSDT","ETHUSDT"]:
        try:result["assets"][sym]=analyze(sym,a.day,a.seconds)
        except Exception as exc:
            result["status"]="PARTIAL_OR_FAILED"
            result["assets"][sym]={"status":"FAILED","error_type":type(exc).__name__,"error":str(exc)}
    a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["status"]!="SUCCESS":raise SystemExit(1)
if __name__=="__main__":main()
