import numpy as np

class Metrics:
    @staticmethod
    def calmar_ratio(equity):
        max_drawdown = np.max(np.maximum.accumulate(equity) - equity)
        annual_return = (equity[-1] / equity[0]) ** (252 / len(equity)) - 1
        return annual_return / max_drawdown if max_drawdown != 0 else np.nan

    @staticmethod
    def sortino_ratio(returns):
        downside = returns[returns < 0].std()
        return returns.mean() / downside * (252 ** 0.5) if downside != 0 else np.nan
