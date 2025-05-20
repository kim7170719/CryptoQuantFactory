import pandas as pd

class Report:
    @staticmethod
    def summary(results):
        summary = {
            'final_equity': results['equity'].iloc[-1],
            'max_drawdown': (results['equity'].cummax() - results['equity']).max(),
            'sharpe': results['returns'].mean() / results['returns'].std() * (252 ** 0.5) if results['returns'].std() != 0 else 0
        }
        return summary
