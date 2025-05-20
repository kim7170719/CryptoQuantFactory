# CryptoQuantFactory

A multi-strategy crypto quant backtest platform supporting RL, DL, multi-factor, traditional, and arbitrage strategies.

## Features
- Multi-strategy (RL/DL/multifactor/traditional/arbitrage)
- Multiple data sources (CoinMarketCap, CoinGecko, CCXT, Yahoo, OKX, Bybit, etc.)
- Multi-asset, multi-timeframe backtest and optimization
- Strategy portfolio, parameter optimization, overfitting test
- Cross-platform (Windows/Mac/Linux)
- **Multi-language support** (EN/ZH/JA/KO)
- **Beautiful, user-friendly Web UI**
- **Detailed changelog and update log**

## Quick Start
- CLI: `python interface/cli.py --strategy strategies/traditional/ma_cross.py --data data/sample.csv`
- Web: `streamlit run interface/web_ui.py`

## Language Switch
- Web sidebar: EN/ZH/JA/KO
- CLI/Web/report/errors all support multi-language

## Security & Risk Control
- API Key encryption (utils/security/crypto.py)
- Order risk control (trading/risk_control.py)
- Paper/live trading isolation (trading/safe_trading.py)

## Documentation
- [中文說明](README.md)
- [API Docs](docs/api.md)
- [FAQ](docs/faq.md)
- [Community](https://github.com/yourname/cryptoquantfactory/discussions)

## Changelog
See `更新.log` for details.
