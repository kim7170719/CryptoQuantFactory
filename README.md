
# CryptoQuantFactory

一個支援強化學習、深度學習、多因子、傳統、套利等多種策略的加密貨幣量化回測平台。

## 主要特點
- 支援多種策略（RL/DL/多因子/傳統/套利）
- 多數據接口（CoinMarketCap、CoinGecko、CCXT、Yahoo、OKX、Bybit等）
- 多幣種、多時間框架回測與優化
- 策略組合、參數優化、過擬合測試
- 跨平台（Windows/Mac/Linux）
- **多國語言支援**（中/英/日/韓，Web/CLI/報告/錯誤訊息）
- **美觀易用的 Web 介面**（多語言、策略選擇、圖形化回測）
- **詳細版本日誌與更新記錄**

## 目錄結構
```
CryptoQuantFactory/
├─ data/                # 數據存儲
├─ datasources/         # 數據接口
├─ strategies/          # 策略模組
├─ backtest/            # 回測引擎
├─ optimizer/           # 優化模組
├─ analysis/            # 結果分析
├─ interface/           # CLI/Web界面
├─ trading/             # 模擬盤/實盤接口
├─ i18n/                # 多國語言包
├─ tests/               # 單元測試
├─ requirements.txt     # 依賴包
├─ README.md            # 說明文件
├─ setup.py             # 安裝腳本
├─ main.py              # 主入口
├─ 更新.log             # 詳細技術更新日誌
```

## 安裝方式
```bash
pip install -r requirements.txt
```

## 快速開始
- CLI: `python interface/cli.py --strategy strategies/traditional/ma_cross.py --data data/sample.csv`
- Web: `streamlit run interface/web_ui.py`

## 多國語言切換
- Web 介面左側可選擇語言（en/zh/ja/ko）
- CLI/Web/報告/錯誤訊息皆支援多語言

## 策略開發
繼承`strategies/base_strategy.py`，實現`generate_signals`與`set_params`方法。

## 數據源配置
見`datasources/`下各模組。

## 版本日誌（Changelog）
- **v0.1.1**：新增多國語言支援（en/zh/ja/ko），Web/CLI/報告/錯誤訊息多語言化
- **v0.1.2**：Web 介面美化，支援多語言切換、策略選擇、圖形化回測

## 詳細技術更新
請見 `更新.log`

## 聯絡/貢獻
歡迎PR與issue！
## 穩定性與擴展性
- 全模組日誌系統（logs/，info/warning/error/debug，見 utils/logging/logger.py）
- 全局異常處理與自定義異常類（見 utils/exception/exception.py）
- 單元測試、集成測試、覆蓋率（pytest, pytest-cov，CI/CD自動化）
- GitHub Actions 自動化測試（.github/workflows/python-app.yml）

## 測試與覆蓋率
- 執行所有測試：`pytest --cov=./ --cov-report=term`
- 覆蓋率報告：`coverage.xml`，CI自動上傳到Codecov

## 版本日誌（Changelog）
- **v0.1.3**：新增日誌系統、異常處理、CI/CD自動化測試、覆蓋率分析

## 實盤安全與風控
- API Key 加密存儲（utils/security/crypto.py，Fernet對稱加密）
- 下單風控（trading/risk_control.py，單筆/日損/持倉限制）
- 實盤/模擬盤隔離與安全下單（trading/safe_trading.py）

## 版本日誌（Changelog）
- **v0.1.4**：新增 API Key 加密、下單風控、實盤/模擬盤隔離與安全下單

## 文件與社群
- 多語言 README（README.md, README.en.md）
- API 文檔（docs/api.md）
- FAQ（docs/faq.md）
- 社群入口：[GitHub Discussions](https://github.com/yourname/cryptoquantfactory/discussions)

## 版本日誌（Changelog）
- **v0.1.5**：新增多語言 README、API 文檔、FAQ、社群入口

## 進階功能
- 插件系統（plugins/，支援用戶自定義策略/數據/分析插件，見 plugins/plugin_manager.py）
- 雲端部署（可用 Docker、Streamlit Cloud、Heroku、AWS、GCP 等）
- 自動化回測排程（可用 crontab、Windows 任務排程、雲端定時器等）

## 版本日誌（Changelog）
- **v0.1.6**：新增插件系統、雲端部署建議、自動化排程建議

## 效能分析與壓力測試
- `tests/performance/test_backtest_performance.py`：大數據量回測效能測試
- `tests/performance/profile_backtest.py`：cProfile 效能分析腳本
- `tests/performance/memory_backtest.py`：memory_profiler 記憶體分析腳本

## 版本日誌（Changelog）
- **v0.2.0**：新增效能分析、壓力測試、記憶體分析腳本

## 兼容性與多平台測試
- `utils/compatibility/check_dependencies.py`：依賴檢查
- `utils/compatibility/python_version_check.py`：Python 版本檢查
- `utils/compatibility/try_except_fallback.py`：安全導入與 fallback
- `tests/compatibility/test_compatibility.py`：自動化兼容性測試

## 版本日誌（Changelog）
- **v0.2.1**：新增依賴檢查、Python 版本檢查、安全導入、兼容性自動化測試

## 錯誤收集與回報
- `utils/logging/error_reporter.py`：錯誤日誌自動收集、可選匿名郵件回報
- `logs/error.log`：集中存放錯誤日誌
- `tests/logs/test_error_reporter.py`：錯誤收集自動化測試

## 版本日誌（Changelog）
- **v0.2.2**：新增錯誤收集與回報系統

## 回歸測試與自動對比
- `tests/regression/test_regression_backtest.py`：回歸測試，對比回測結果與歷史基準，異常自動報警

## 版本日誌（Changelog）
- **v0.2.3**：新增回歸測試與自動對比

## 數據接口模組完善
- ccxt_source.py：多交易所、多幣種、多時間框架K線拉取，異常處理
- cmc_source.py：CoinMarketCap API拉取歷史K線，API Key配置
- coingecko_source.py：CoinGecko API拉取歷史K線，多幣種、多時間框架
- yahoo_source.py：Yahoo Finance拉取多幣種、多時間框架
- okx_source.py/bybit_source.py：OKX/Bybit API拉取K線
- cache.py：本地快取，避免重複拉取

## 版本日誌（Changelog）
- **v0.3.0**：數據接口模組完善，所有數據源可用，支援快取

## 策略模組完善
- multifactor/momentum_value.py：動量+價值多因子策略，支援多因子自定義
- arbitrage/triangular.py：三角套利策略，完善多幣種套利邏輯
- arbitrage/calendar.py：跨期套利策略，完善合約套利邏輯
- rl_dl/lstm.py：LSTM 策略，完善訓練、預測流程
- rl_dl/dqn.py：DQN 策略，完善訓練、預測流程

## 版本日誌（Changelog）
- **v0.3.1**：策略模組完善，所有策略可用

## 回測引擎模組完善
- engine.py：單幣種回測，支援交易成本、滑點、資金管理
- portfolio.py：多策略組合權重分配、績效合併
- multi_asset_engine.py：多幣種同時回測，獨立/合併資金池
- multi_timeframe_engine.py：多時間框架回測，主/輔信號融合
- event_engine.py：事件驅動回測，支援自定義事件
- slippage.py：多種滑點模型（固定、隨機）
- capital_management.py：多種資金管理策略（定額、定比、最大槓桿）

## 版本日誌（Changelog）
- **v0.3.2**：回測引擎模組完善，支援多幣種、多時間框架、滑點、資金管理

## 優化模組完善
- optimizer.py：Optuna 參數優化，異常處理
- overfit_test.py：Walk Forward 過擬合測試
- grid_search.py：網格搜索優化
- genetic.py：遺傳算法優化（骨架，需集成GA庫）
- cross_validation.py：交叉驗證（骨架，需完善CV邏輯）

## 版本日誌（Changelog）
- **v0.3.3**：優化模組完善，支援多種優化與過擬合測試

## 分析模組完善
- report.py：回測績效摘要（最終資產、最大回撤、夏普比率）
- plot.py：資產曲線可視化
- metrics.py：Calmar、Sortino等績效指標
- compare.py：多策略/多幣種績效對比圖
- export.py：報告導出（Excel、CSV）

## 版本日誌（Changelog）
- **v0.3.4**：分析模組完善，支援多種績效指標、可視化、報告導出

## 交易模組完善
- paper_trading.py：模擬盤下單、持倉、歷史記錄
- live_trading.py：實盤下單、查詢持倉，API對接
- risk_control.py：下單風控（單筆/日損/持倉限制）
- safe_trading.py：實盤/模擬盤隔離與安全下單
- utils/security/crypto.py：API Key加密存儲，異常處理

## 版本日誌（Changelog）
- **v0.3.5**：交易模組完善，支援模擬盤、實盤、風控、API加密

## 插件系統完善
- plugin_manager.py：插件加載、註冊、熱插拔、異常處理
- sample_strategy_plugin.py：策略插件範例

## 版本日誌（Changelog）
- **v0.3.6**：插件系統完善，支援插件加載、註冊、熱插拔

## Web/CLI 介面完善
- cli.py：多語言、策略選擇、數據上傳、回測、報告
- web_ui.py：多語言、策略選擇、圖形化回測、績效報告

## 版本日誌（Changelog）
- **v0.3.7**：Web/CLI 介面完善，支援多語言、策略選擇、圖形化回測


# CryptoQuantFactory
