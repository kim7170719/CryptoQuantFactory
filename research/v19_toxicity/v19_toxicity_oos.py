#!/usr/bin/env python3
"""V19 ex-ante 200ms Maker quotes on genuine Tardis Binance Futures L2/trades.
Counterfactual trade-through only; NO FIFO proof or actual account fills.
Does not save licensed raw events.
"""
import argparse,bisect,collections,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"v16_tardis_real_ticks"))
from v16_tardis_first_minute import fetch
TRAIN=("2024-04-01","2025-06-01")
TEST=("2025-08-01","2025-10-01")
SYMBOLS=("BTCUSDT","ETHUSDT")
RULES=("all","imb0","imb20","micro0","micro02","flow20","imbmicro","imbflow")
def reconstruct(rows):
    bids={};asks={};out=[];last=None;last_snap=False;ready=False;bad=0;snaps=0
    def emit(t):
        nonlocal bad
        if not ready:return
        if not bids or not asks:bad+=1;return
        b=max(bids);a=min(asks)
        if b<=0 or a<=b:bad+=1;return
        bb=bids[b];aa=asks[a];mid=(a+b)/2
        b5=sum(p*bids[p] for p in sorted(bids,reverse=True)[:5])
        a5=sum(p*asks[p] for p in sorted(asks)[:5])
        micro=(a*bb+b*aa)/(bb+aa) if bb+aa else mid
        out.append((t,b,a,(b5-a5)/(b5+a5) if b5+a5 else 0,10000*(micro-mid)/mid,10000*(a-b)/mid))
    for r in rows:
        t=int(r["local_timestamp"]);snap=str(r["is_snapshot"]).lower()=="true"
        if last is not None and t<last:raise ValueError("REVERSED_BOOK_TIME")
        if last is not None and t!=last and not last_snap:emit(last)
        if snap and not last_snap:bids={};asks={};ready=False;snaps+=1
        if not snap and last_snap:ready=True
        d=bids if r["side"].lower()=="bid" else asks if r["side"].lower()=="ask" else None
        if d is None:raise ValueError("BAD_L2_SIDE")
        p=float(r["price"]);q=float(r["amount"])
        if not math.isfinite(p) or p<=0 or not math.isfinite(q) or q<0:raise ValueError("BAD_L2_LEVEL")
        if q==0:d.pop(p,None)
        else:d[p]=q
        last=t;last_snap=snap
    if last is not None and not last_snap:emit(last)
    if bad:raise ValueError("INVALID_BBO_GROUPS_"+str(bad))
    if len(out)<10:raise ValueError("INSUFFICIENT_BBO")
    return out,{"snapshots":snaps,"groups":len(out),"invalid":bad}
def quotes(book,tape,symbol):
    """At 8s scheduled qtime submit two quotes with PREVIOUS known BBO and past flow.
    Active at qtime+200ms, expire at qtime+2s; exit at 5s after trade-through.
    Keep both potential sides; rule chooses earliest ALLOWED observed crossing.
    """
    tick=.1 if symbol=="BTCUSDT" else .01
    bt=[x[0] for x in book]
    tr=[r for r in tape if r["side"].lower() in ("buy","sell") and float(r["price"])>0 and float(r["amount"])>0]
    tt=[int(r["local_timestamp"]) for r in tr]
    if not tt:raise ValueError("NO_TRADE_TAPE")
    if any(b<a for a,b in zip(tt,tt[1:])):raise ValueError("TRADE_TIME_REVERSED")
    start=max(bt[0]+1000000,tt[0]+1000000)
    end=min(bt[-1],tt[-1])-8000000
    accepted=[];skip=collections.Counter();q=0
    while start+q*8000000<end:
        at=start+q*8000000;q+=1
        j=bisect.bisect_left(bt,at)-1
        if j<0 or at-bt[j]>1000000:skip["STALE_BBO"]+=1;continue
        _,bid,ask,imb,micro,spread=book[j]
        flowstart=bisect.bisect_left(tt,at-2000000)
        flowend=bisect.bisect_left(tt,at)
        old=tr[flowstart:flowend]
        buy=sum(float(r["price"])*float(r["amount"]) for r in old if r["side"].lower()=="buy")
        sell=sum(float(r["price"])*float(r["amount"]) for r in old if r["side"].lower()=="sell")
        flow=(buy-sell)/(buy+sell) if buy+sell else 0
        first={}
        l=bisect.bisect_left(tt,at+200000)
        h=bisect.bisect_left(tt,at+2000000)
        for r in tr[l:h]:
            ts=int(r["local_timestamp"])
            maker=1 if r["side"].lower()=="sell" else -1
            if maker in first:continue
            quote=bid if maker==1 else ask
            px=float(r["price"]);notional=px*float(r["amount"])
            if notional<100:continue
            through=px<=quote-.9*tick if maker==1 else px>=quote+.9*tick
            if not through:continue
            k=bisect.bisect_left(bt,ts+5000000)
            if k>=len(book) or book[k][0]-ts>6000000:skip["NO_FUTURE_BBO"]+=1;continue
            exitpx=book[k][1] if maker==1 else book[k][2]
            gross=maker*(exitpx-quote)/quote*10000
            first[maker]={"symbol":symbol,"q":q,"qtime":at,"t":ts,"gross_bps":gross,
                          "net_bps":gross-7,
                          "imb":round(maker*imb,6),"micro":round(maker*micro,6),
                          "flow":round(maker*flow,6),"spread_bps":round(spread,6)}
        if not first:skip["NO_CROSSING"]+=1
        accepted.extend(first.values())
    skip["QUOTE_CYCLES"]=q
    return accepted,dict(skip)
def permitted(r,name):
    return {"all":True,"imb0":r["imb"]>=0,"imb20":r["imb"]>=.2,
            "micro0":r["micro"]>=0,"micro02":r["micro"]>=.02,
            "flow20":r["flow"]>=.2,
            "imbmicro":r["imb"]>=0 and r["micro"]>=0,
            "imbflow":r["imb"]>=0 and r["flow"]>=.2}[name]
def score(events,name):
    groups=collections.defaultdict(list)
    for e in events:
        if permitted(e,name):groups[(e["symbol"],e["qtime"])].append(e)
    chosen=[min(v,key=lambda e:e["t"]) for v in groups.values()]
    return {"fills":len(chosen),"pnl_usdt":round(sum(e["net_bps"]*.01 for e in chosen),6),
            "gross_usdt":round(sum(e["gross_bps"]*.01 for e in chosen),6),
            "mean_net_bps":round(sum(e["net_bps"] for e in chosen)/len(chosen),4) if chosen else None}
def evaluate(data):
    result={}
    for sym in SYMBOLS:
        tr=[e for d in TRAIN for e in data[d][sym]["events"]]
        ho=[e for d in TEST for e in data[d][sym]["events"]]
        experiments=[{"rule":rule,"train":score(tr,rule),"holdout":score(ho,rule),
           "train_each":[score(data[d][sym]["events"],rule) for d in TRAIN],
           "holdout_each":[score(data[d][sym]["events"],rule) for d in TEST]} for rule in RULES]
        eligible=[r for r in experiments if r["train"]["fills"]>=8]
        best=max(eligible,key=lambda r:r["train"]["pnl_usdt"]) if eligible else None
        admitted=bool(best and best["train"]["pnl_usdt"]>0 and all(v["pnl_usdt"]>0 for v in best["train_each"]))
        result[sym]={"train_candidates":len(tr),"holdout_candidates":len(ho),
          "baseline_no_filter":experiments[0],"selected_best":best,"all_rules":experiments,
          "train_gate_passed":admitted,"production_decision":"NO_TRADE",
          "research_only_oos_if_trained":best["holdout"]["pnl_usdt"] if admitted else None}
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);ap.add_argument("--seconds",type=int,default=90)
    args=ap.parse_args()
    data={};audit=[]
    try:
        for day in TRAIN+TEST:
            data[day]={}
            for sym in SYMBOLS:
                l2,url=fetch(sym,day,"incremental_book_L2",args.seconds)
                trade,url2=fetch(sym,day,"trades",args.seconds)
                book,quality=reconstruct(l2)
                gaps=[b[0]-a[0] for a,b in zip(book,book[1:])]
                if gaps and max(gaps)>5000000:raise ValueError("BBO_GAP_GT_5S")
                events,skips=quotes(book,trade,sym)
                data[day][sym]={"events":events}
                audit.append({"date":day,"symbol":sym,"l2_rows":len(l2),"trade_rows":len(trade),
                  "bbo":quality,"candidate_sides":len(events),"quotes":skips.get("QUOTE_CYCLES",0),
                  "max_bbo_gap_us":max(gaps) if gaps else 0,"skips":skips,
                  "book_url":url,"trade_url":url2})
        out={"status":"SUCCESS","method":"EX_ANTE_8SEC_MAKER_QUOTING_REAL_L2_AND_TRADES_FILL_PROXY",
             "train_dates":TRAIN,"holdout_dates":TEST,"seconds_per_day":args.seconds,
             "fee_bps":{"maker":2,"taker_exit":5},"audit":audit,"results":evaluate(data),
             "live_orders_submitted":False,"fifo_confirmed":False,
             "risk_note":"EIGHT 90-second first-of-month windows cannot establish annual positive expectancy.",
             "signal_note":"All quote/filter features at fixed qtime, historical outcomes after 200ms activation."}
    except Exception as e:
        out={"status":"FAILED","reason":str(e),"type":type(e).__name__,"audit":audit}
    Path(args.out).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"status":out["status"],"summary":out.get("results",{}),"error":out.get("reason")},indent=2))
    if out["status"]!="SUCCESS":raise SystemExit(1)
if __name__=="__main__":main()
