import pandas as pd

class Export:
    @staticmethod
    def to_excel(results, filename):
        results.to_excel(filename)
    @staticmethod
    def to_csv(results, filename):
        results.to_csv(filename)
