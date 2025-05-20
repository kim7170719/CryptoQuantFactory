import matplotlib.pyplot as plt

class Compare:
    @staticmethod
    def multi_equity_curves(results_dict):
        plt.figure(figsize=(12, 6))
        for name, result in results_dict.items():
            plt.plot(result['equity'], label=name)
        plt.legend()
        plt.title('Multi-Strategy/Asset Equity Curves')
        plt.show()
