import streamlit as st
import pandas as pd
import os
from i18n.i18n import I18N
from analysis.report import Report
from analysis.plot import Plot
from strategies.traditional.ma_cross import MovingAverageCrossStrategy
from strategies.traditional.rsi import RSIStrategy
from strategies.traditional.macd import MACDStrategy
from strategies.traditional.bollinger import BollingerBandsStrategy

lang = st.sidebar.selectbox('Language', ['en', 'zh', 'ja', 'ko'])
_ = I18N(lang, os.path.join(os.path.dirname(__file__), '../i18n')).t

st.title(_('welcome'))
st.write(_('start_cli'))

strategy_map = {
    _('Moving Average Cross'): MovingAverageCrossStrategy,
    _('RSI'): RSIStrategy,
    _('MACD'): MACDStrategy,
    _('Bollinger Bands'): BollingerBandsStrategy
}
strategy_name = st.sidebar.selectbox(_('strategy'), list(strategy_map.keys()))

uploaded_file = st.file_uploader(_('data'))
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    strategy = strategy_map[strategy_name]()
    st.write(_('summary'))
    if st.button(_('run')):
        from backtest.engine import BacktestEngine
        engine = BacktestEngine(strategy, data)
        results = engine.run()
        st.write(Report.summary(results))
        Plot.equity_curve(results)
