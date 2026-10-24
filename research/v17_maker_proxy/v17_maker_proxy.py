#!/usr/bin/env python3
"""V17: REAL Binance Futures Tardis book & trade events, simulated Maker fill proxy.
No exchange execution proof, no live orders. Never store/publish raw licensed ticks.
"""
import argparse,bisect,json,math,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"v16_tardis_real_ticks"))
from v16_tardis_first_minute import fetch,book_series

def at(book,t):
    idx=bisect.bisect_left(book["times"],t)-1
    if idx<0 or t-book["times"][idx]>1_000_000:return None
    return (book["bids"][idx],book["asks"][idx],(book["bids"][idx]+book["asks"][idx])/2)

def tickround(p,tick,buy):
    n=p/tick
    return (math.floor(n+1e-7) if buy else math.ceil(n-1e-7))*tick

def test_strategy(book,trades,symbol,variant):
    if variant not in ("top","wide_1bp","wide_5bp","flow_1bp"):raise ValueError("BAD_STRATEGY")
    if len(book["times"])<2:raise ValueError("NOT_ENOUGH_BOOK")
    tick=.1 if symbol=="BTCUSDT" else .01
    maker=.0002;taker=.0005
    first_t=int(trades[0]["local_timestamp"]);last_t=int(trades[-1]["local_timestamp"])
    start=max(book["times"][0]+500_000,first_t+200_000)
    end=min(book["times"][-1],last_t)-500_000
    if end-start<2_000_000:raise ValueError("SHORT_SAMPLE")
    cash=10000.;position=0.;fees=0.;peak=10000.;mdd=0.
    maker_fills=0;hedges=0;quotes=0;no_bbo=0;side_fills={"buy":0,"sell":0}
    outstanding=None;hedge_after=None;next_quote=start;last_flow=[]
    def update(mid):
        nonlocal peak,mdd
        net=cash+position*mid;peak=max(peak,net);mdd=max(mdd,(peak-net)/peak)
    for x in trades:
        t=int(x["local_timestamp"])
        if t<start:continue
        if t>end:break
        aggressor=x["side"].lower()
        if aggressor not in ("buy","sell"):continue
        trade_px=float(x["price"]);trade_notional=trade_px*float(x["amount"])
        if hedge_after is not None and t>=hedge_after and abs(position)>0:
            price=at(book,t)
            if price is not None:
                b,a,mid=price
                hedge_px=b if position>0 else a
                cost=abs(position*hedge_px)*taker
                cash+=position*hedge_px-cost
                fees+=cost;position=0.;hedges+=1;hedge_after=None;update(mid)
        last_flow=[(ts,side,nom) for ts,side,nom in last_flow if t-ts<=2_000_000]
        while next_quote<=t:
            outstanding=None
            market=at(book,next_quote)
            if market is None:no_bbo+=1
            elif abs(position)<1e-10:
                b,a,mid=market
                extra={"top":0,"wide_1bp":1,"wide_5bp":5,"flow_1bp":1}[variant]
                bid=tickround(b*(1-extra/1e4),tick,True)
                ask=tickround(a*(1+extra/1e4),tick,False)
                positive=True;negative=True
                if variant=="flow_1bp":
                    buyv=sum(n for _,side,n in last_flow if side=="buy")
                    sellv=sum(n for _,side,n in last_flow if side=="sell")
                    imb=(buyv-sellv)/(buyv+sellv) if buyv+sellv else 0
                    positive=imb>.2;negative=imb<-.2
                if bid<ask:
                    outstanding=(bid,ask,next_quote+200_000,next_quote+2_000_000,positive,negative)
                    quotes+=1
            next_quote+=2_000_000
        if outstanding and outstanding[2]<=t<outstanding[3] and abs(position)<1e-10:
            bid,ask,_,_,buy_ok,sell_ok=outstanding
            # Strict >= 1 tick trade-through and enough historical aggressor notional.
            if aggressor=="sell" and buy_ok and trade_px<=bid-.9*tick and trade_notional>=100:
                side=1;px=bid
            elif aggressor=="buy" and sell_ok and trade_px>=ask+.9*tick and trade_notional>=100:
                side=-1;px=ask
            else:side=0
            if side:
                signed_qty=side*100/px;cash-=signed_qty*px+100*maker
                position+=signed_qty;fees+=100*maker
                maker_fills+=1;side_fills["buy" if side==1 else "sell"]+=1
                hedge_after=t+200_000;outstanding=None
                market=at(book,t)
                update(market[2] if market else px)
        last_flow.append((t,aggressor,trade_notional))
    if abs(position)>1e-10:
        price=at(book,end)
        if price is None:raise ValueError("UNRESOLVED_END_INVENTORY")
        b,a,mid=price
        px=b if position>0 else a
        fee=abs(position*px)*taker
        cash+=position*px-fee;fees+=fee;position=0;hedges+=1;update(mid)
    pnl=cash-10000
    return {"strategy":variant,"pnl_usdt":round(pnl,6),"mdd_pct":round(mdd*100,6),
     "maker_fills":maker_fills,"taker_hedges":hedges,"simulated_quote_cycles":quotes,
     "fees_usdt":round(fees,6),"rejected_quote_missing_recent_bbo":no_bbo,
     "buy_fills":side_fills["buy"],"sell_fills":side_fills["sell"],
     "fee_assumptions_bps":{"maker":2,"taker_hedge":5},
     "must_not_interpret_as_real_fill":True}

def analyze(symbol,day,seconds):
    bookrows,l2url=fetch(symbol,day,"incremental_book_L2",seconds)
    rows,tradesurl=fetch(symbol,day,"trades",seconds)
    book=book_series(bookrows)
    if len(book["times"])<10:raise ValueError("NO_CONTINUOUS_L2_BBO")
    if book["bad_bbo"]>0:raise ValueError("INVALID_BBO_GROUPS_FOUND_"+str(book["bad_bbo"]))
    gaps=[y-x for x,y in zip(book["times"],book["times"][1:])]
    if gaps and max(gaps)>5_000_000:raise ValueError("BOOK_GAP_GT_5S")
    for b,a in zip(book["bids"],book["asks"]):
        if b>=a:raise ValueError("CROSSED_BOOK")
    results=[test_strategy(book,rows,symbol,c) for c in ("top","wide_1bp","wide_5bp","flow_1bp")]
    return {"symbol":symbol,"real_l2_rows":len(bookrows),"real_trade_rows":len(rows),
     "real_bbo_groups":len(book["times"]),"invalid_bbo_groups":book["bad_bbo"],"valid_bbo_fraction_of_book_groups":round(len(book["times"])/(len(book["times"])+book["bad_bbo"]),8),
     "median_actual_spread_bps":round(statistics.median(1e4*(a-b)/((a+b)/2) for b,a in zip(book["bids"],book["asks"])),8),
     "source":{"l2":l2url,"trades":tradesurl},"simulation":results,
     "cash_benchmark_pnl_usdt":0,
     "limitations":["Genuine L2 and trades; strategy quotes and fills are hypothetical",
       "No exchange FIFO queue priority","20-90 second observation window",
       "Tardis normalized data lacks explicit Binance U/u sequence IDs",
       "No funding settles within window; not a long-run expected-value study",
       "Static 2 bps Maker, 5 bps taker fee assumptions; no options hedging"]}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--day",default="2025-08-01")
    p.add_argument("--seconds",type=int,default=90)
    p.add_argument("--out",default="v17_maker_proxy_result.json")
    args=p.parse_args()
    out={"method":"observed_real_binance_l2_and_trade_through_SIMULATED_maker","day":args.day,
       "window_seconds":args.seconds,"status":"SUCCESS","symbols":{}}
    for sym in ("BTCUSDT","ETHUSDT"):
        try:out["symbols"][sym]=analyze(sym,args.day,args.seconds)
        except Exception as e:
            out["symbols"][sym]={"status":"FAILED","reason":str(e),"type":type(e).__name__}
            out["status"]="PARTIAL_OR_FAILED"
    Path(args.out).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if out["status"]!="SUCCESS":raise SystemExit(1)
if __name__=="__main__":main()
