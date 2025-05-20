# CryptoQuantFactory API Documentation

## Strategy Base Class
- `BaseStrategy.generate_signals(data)`
- `BaseStrategy.set_params(**params)`

## Data Sources
- `CCXTSource.fetch_ohlcv(symbol, timeframe, since, limit)`
- `CMCSource.fetch_ohlcv(symbol, convert)`
- `CoinGeckoSource.fetch_ohlcv(coin_id, vs_currency, days)`
- `YahooSource.fetch_ohlcv(symbol, start, end, interval)`

## Backtest Engine
- `BacktestEngine(strategy, data, initial_cash, fee)`
- `BacktestEngine.run()`

## Optimizer
- `StrategyOptimizer(strategy_class, data, param_space, n_trials)`
- `StrategyOptimizer.optimize()`

## Trading
- `PaperTrading.send_order(signal, price, size)`
- `LiveTrading.send_order(signal, price, size)`
- `SafeTrading.send_order(signal, price, size, account)`

## Risk Control
- `RiskControl.check_order(order, account)`

## More details see source code and README.
