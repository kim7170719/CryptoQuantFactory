import streamlit as st
import pandas as pd
from backtest.engine import BacktestEngine
from analysis.report import Report
from analysis.plot import Plot

st.title('CryptoQuantFactory Web Interface')

uploaded_file = st.file_uploader('Upload CSV data')
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    # 這裡僅示例，實際應可選策略
    from strategies.traditional.ma_cross import MovingAverageCrossStrategy
    strategy = MovingAverageCrossStrategy()
    engine = BacktestEngine(strategy, data)
    results = engine.run()
    st.write(Report.summary(results))
    Plot.equity_curve(results)
