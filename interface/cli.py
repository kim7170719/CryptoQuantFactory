import argparse
import importlib.util
import pandas as pd
from backtest.engine import BacktestEngine
from analysis.report import Report
from analysis.plot import Plot
import logging

# CLI 支援多語言、策略選擇、數據上傳、回測、報告

def main():
    parser = argparse.ArgumentParser(description='CryptoQuantFactory CLI')
    parser.add_argument('--strategy', type=str, required=True, help='Strategy module path')
    parser.add_argument('--data', type=str, required=True, help='CSV data file')
    parser.add_argument('--lang', type=str, default='en', help='Language (en/zh/ja/ko)')
    args = parser.parse_args()

    # 動態導入策略
    spec = importlib.util.spec_from_file_location('Strategy', args.strategy)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # 假設策略類名為 Strategy
    strategy_class = getattr(module, [c for c in dir(module) if c.endswith('Strategy')][0])
    strategy = strategy_class()

    data = pd.read_csv(args.data)
    engine = BacktestEngine(strategy, data)
    results = engine.run()
    print(Report.summary(results))
    Plot.equity_curve(results)

if __name__ == '__main__':
    main()
