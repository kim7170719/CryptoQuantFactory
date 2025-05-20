import matplotlib.pyplot as plt

class Plot:
    @staticmethod
    def equity_curve(results):
        plt.figure(figsize=(10, 5))
        plt.plot(results['equity'])
        plt.title('Equity Curve')
        plt.xlabel('Time')
        plt.ylabel('Equity')
        plt.show()
