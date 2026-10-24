#!/usr/bin/env python3
"""V18 true Binance Futures L2/trades, HYPOTHETICAL maker-to-maker inventory-netting.
No actual user orders, FIFO proof, positive-alpha assertion, or raw data redistribution.
"""
import argparse,collections,json,math,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"v16_tardis_real_ticks"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"v17_maker_proxy"))
from v16_tardis_first_minute import fetch,book_series
from v17_maker_proxy import at,tickround
TICK={"BTCUSDT":.1,"ETHUSDT":.01}
LAG_US=200_000;QUOTE_PERIOD_US=2_000_000;CAPITAL=10000.;ORDER_USDT=100.

def config_set():
    return [{"width_bps":w,"hold_s":hold,"flow_mode":mode}
            for w in (0,0.5,1,2,3) for hold in (1,5,15,45)
            for mode in ("none","follow","fade")]

def simulate(book,trades,symbol,cfg,maker_bps=2,taker_bps=5):
    if symbol not in TICK:raise ValueError("BAD_SYMBOL")
    if book.get("bad_bbo",0):raise ValueError("INVALID_BOOK_BLOCK")
    if len(book["times"])<10:raise ValueError("TOO_FEW_BBO")
    tick=TICK[symbol]
    first=max(book["times"][0]+500_000,int(trades[0]["local_timestamp"])+200_000)
    end=min(book["times"][-1],int(trades[-1]["local_timestamp"]))-500_000
    if end-first<3_000_000:raise ValueError("SHORT_WINDOW")
    cash=CAPITAL;pos=0.;peak=CAPITAL;mdd=0.;fees=0.;maker_vol=0.;taker_vol=0.
    entry_fills=0;maker_exits=0;taker_exits=0;entry_side=collections.Counter()
    last_entry=None;quotes=None;next_quote=first;missing_bbo=0;crossed_reject=0;maker_pnl=[]
    recent=collections.deque()
    def nav(mid):
        nonlocal peak,mdd
        x=cash+pos*mid;peak=max(peak,x);mdd=max(mdd,(peak-x)/peak)
    def taker_close(t):
        nonlocal cash,pos,fees,taker_vol,taker_exits,quotes,last_entry
        if abs(pos)<1e-12:return True
        x=at(book,t)
        if x is None:return False
        bid,ask,mid=x;px=bid if pos>0 else ask
        volume=abs(pos*px);f=volume*taker_bps/1e4
        cash+=pos*px-f;fees+=f;taker_vol+=volume;taker_exits+=1
        pos=0.;last_entry=None;quotes=None;nav(mid)
        return True
    def flow_before(qt):
        eligible=[(t,s,v) for t,s,v in recent if t<qt and qt-t<=2_000_000]
        buy=sum(v for _,s,v in eligible if s=="buy")
        sell=sum(v for _,s,v in eligible if s=="sell")
        return (buy-sell)/(buy+sell) if (buy+sell)>0 else 0
    for row in trades:
        t=int(row["local_timestamp"])
        if t<first:continue
        if t>end:break
        side=row["side"].lower()
        if side not in ("buy","sell"):continue
        price=float(row["price"]);amount=float(row["amount"])
        if not(math.isfinite(price) and price>0 and math.isfinite(amount) and amount>0):
            raise ValueError("BAD_TRADE")
        while recent and t-recent[0][0]>4_000_000:recent.popleft()
        if pos and last_entry is not None and t>=last_entry+cfg["hold_s"]*1_000_000:
            if not taker_close(t):raise ValueError("CANNOT_HEDGE_STALE_BOOK")
        while next_quote<=t:
            qtime=next_quote;next_quote+=QUOTE_PERIOD_US;quotes=None
            bbo=at(book,qtime)
            if bbo is None:missing_bbo+=1;continue
            bid,ask,mid=bbo
            if bid>=ask:crossed_reject+=1;continue
            f=flow_before(qtime);mode=cfg["flow_mode"]
            if pos:
                # Rest a maker EXIT at the opposite best side without adding exposure.
                exit_side="sell" if pos>0 else "buy"
                px=tickround(ask if pos>0 else bid,tick,pos<0)
                quotes={"side":exit_side,"px":px,"vol":abs(pos*px),
                        "active":qtime+LAG_US,"end":qtime+QUOTE_PERIOD_US,"exit":True}
            else:
                spread=cfg["width_bps"]/1e4
                bb=tickround(bid*(1-spread),tick,True)
                aa=tickround(ask*(1+spread),tick,False)
                allowed={"buy":True,"sell":True}
                if mode!="none":
                    if abs(f)<.2:allowed={"buy":False,"sell":False}
                    elif mode=="follow":allowed={"buy":f>0,"sell":f<0}
                    elif mode=="fade":allowed={"buy":f<0,"sell":f>0}
                if bb>=aa:crossed_reject+=1;continue
                quotes={"side":"both","bid":bb,"ask":aa,"allowed":allowed,
                        "active":qtime+LAG_US,"end":qtime+QUOTE_PERIOD_US,"exit":False}
        if quotes and quotes["active"]<=t<quotes["end"]:
            aggressor_notional=price*amount
            qside=None;px=None
            if quotes["exit"]:
                if pos>0 and side=="buy" and price>=quotes["px"]+.9*tick:
                    qside="sell";px=quotes["px"]
                elif pos<0 and side=="sell" and price<=quotes["px"]-.9*tick:
                    qside="buy";px=quotes["px"]
                if qside and aggressor_notional>=abs(pos*px):
                    v=abs(pos*px);f=v*maker_bps/1e4
                    cash+=pos*px-f;fees+=f;maker_vol+=v;maker_exits+=1
                    pos=0.;quotes=None;last_entry=None
                    bbo=at(book,t);nav(bbo[2] if bbo else px)
            elif not pos:
                if side=="sell" and quotes["allowed"]["buy"] and price<=quotes["bid"]-.9*tick:
                    qside="buy";px=quotes["bid"]
                elif side=="buy" and quotes["allowed"]["sell"] and price>=quotes["ask"]+.9*tick:
                    qside="sell";px=quotes["ask"]
                if qside and aggressor_notional>=ORDER_USDT:
                    direction=1 if qside=="buy" else -1
                    q=direction*ORDER_USDT/px
                    cash-=q*px+ORDER_USDT*maker_bps/1e4
                    pos=q;fees+=ORDER_USDT*maker_bps/1e4;maker_vol+=ORDER_USDT
                    entry_side[qside]+=1;entry_fills+=1;last_entry=t;quotes=None
                    bbo=at(book,t);nav(bbo[2] if bbo else px)
        bbo=at(book,t)
        if bbo:nav(bbo[2])
        recent.append((t,side,price*amount))
    if pos and not taker_close(end):raise ValueError("CANNOT_CLOSE_TERMINAL_INVENTORY")
    if pos:raise ValueError("NONZERO_END_POSITION")
    gross=cash-CAPITAL+fees
    break_even_maker_bps=(gross-taker_vol*taker_bps/1e4)*1e4/maker_vol if maker_vol else None
    return {"config":cfg,"pnl_usdt":round(cash-CAPITAL,6),"gross_before_all_fees_usdt":round(gross,6),
       "fee_usdt":round(fees,6),"mdd_pct":round(mdd*100,6),
       "entries":entry_fills,"maker_exits":maker_exits,"taker_exits":taker_exits,
       "maker_notional_usdt":round(maker_vol,3),"taker_notional_usdt":round(taker_vol,3),
       "maker_buy_entries":entry_side["buy"],"maker_sell_entries":entry_side["sell"],
       "zero_delta_at_end":abs(pos)<1e-12,
       "missed_quote_due_stale_bbo":missing_bbo,"rejected_crossed_quote":crossed_reject,
       "break_even_maker_fee_bps_given_5bps_taker":round(break_even_maker_bps,4) if break_even_maker_bps is not None else None,
       "method":"CONSERVATIVE_PRICE_THROUGH_FILL_PROXY_NOT_FIFO"}

def run(day,seconds):
    z={"date":day,"window_seconds":seconds,"data":"Tardis actual historical Binance Futures L2 and trades",
       "fill_model":"Hypothetical maker price-trade-through; 200ms latency; no FIFO proof",
       "assumed_maker_bps":2,"assumed_taker_bps":5,"status":"SUCCESS","assets":{}}
    for symbol in ("BTCUSDT","ETHUSDT"):
        try:
            depth,url1=fetch(symbol,day,"incremental_book_L2",seconds)
            tape,url2=fetch(symbol,day,"trades",seconds)
            book=book_series(depth)
            if not book["times"] or book["bad_bbo"]:raise ValueError("INVALID_OR_EMPTY_BBO")
            gaps=[b-a for a,b in zip(book["times"],book["times"][1:])]
            if gaps and max(gaps)>5_000_000:raise ValueError("L2_BOOK_TIME_GAP_GT_5S")
            runs=[simulate(book,tape,symbol,cfg) for cfg in config_set()]
            z["assets"][symbol]={"l2_rows":len(depth),"tape_rows":len(tape),
                 "bbo_event_groups":len(book["times"]),"invalid_bbo":book["bad_bbo"],
                 "snapshots":book["snapshots"],"source_depth_url":url1,"source_trades_url":url2,
                 "results":runs,"cash_benchmark_pnl_usdt":0}
        except Exception as exc:
            z["assets"][symbol]={"status":"FAILED","type":type(exc).__name__,"error":str(exc)}
            z["status"]="PARTIAL_OR_FAILED"
    return z
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--day",required=True);ap.add_argument("--seconds",type=int,default=90)
    ap.add_argument("--out",required=True);a=ap.parse_args()
    out=run(a.day,a.seconds)
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({sym:{"status":v.get("status","OK"),"runs":len(v.get("results",[]))} for sym,v in out["assets"].items()}))
    if out["status"]!="SUCCESS":raise SystemExit(1)
if __name__=="__main__":main()
