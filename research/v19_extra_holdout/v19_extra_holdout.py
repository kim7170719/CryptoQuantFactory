#!/usr/bin/env python3
"""Extra completely untouched Tardis public free L2 sample dates, V19 frozen rules.
Real observed Binance Futures book and trades; hypothetical fills. No raw data redistribution.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"v19_toxicity"))
from v19_toxicity_oos import fetch,reconstruct,quotes,score,RULES,SYMBOLS
def run(day,seconds):
    out={"date":day,"seconds":seconds,"status":"SUCCESS","symbols":{}}
    for sym in SYMBOLS:
        try:
            l2,url=fetch(sym,day,"incremental_book_L2",seconds)
            trades,tape_url=fetch(sym,day,"trades",seconds)
            book,quality=reconstruct(l2)
            gaps=[b[0]-a[0] for a,b in zip(book,book[1:])]
            if gaps and max(gaps)>5_000_000:raise ValueError("GAP_OVER_5S")
            potential,skip=quotes(book,trades,sym)
            out["symbols"][sym]={"depth_rows":len(l2),"trade_rows":len(trades),
               "book":quality,"quote_cycles":skip["QUOTE_CYCLES"],
               "possible_price_through_sides":len(potential),
               "rules":{name:score(potential,name) for name in RULES},
               "book_source":url,"trade_source":tape_url}
        except Exception as e:
            out["symbols"][sym]={"status":"FAILED","reason":str(e)}
            out["status"]="FAIL_CLOSED"
    return out
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--day",required=True);ap.add_argument("--seconds",type=int,default=90)
    ap.add_argument("--out",required=True);a=ap.parse_args()
    result=run(a.day,a.seconds)
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({s:v.get("rules",{}).get("all",v.get("reason")) for s,v in result["symbols"].items()},indent=2))
    if result["status"]!="SUCCESS":raise SystemExit(1)
if __name__=="__main__":main()
