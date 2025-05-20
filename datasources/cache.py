import os
import pandas as pd
import pickle

class DataCache:
    def __init__(self, cache_dir='data/cache'):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def save(self, key, data):
        path = os.path.join(self.cache_dir, f'{key}.pkl')
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load(self, key):
        path = os.path.join(self.cache_dir, f'{key}.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        return None
