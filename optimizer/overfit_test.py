import numpy as np
import logging

class OverfitTest:
    @staticmethod
    def walk_forward(data, strategy_class, param_space, n_splits=5):
        split_size = len(data) // n_splits
        results = []
        for i in range(n_splits):
            train = data.iloc[:split_size*(i+1)]
            test = data.iloc[split_size*(i+1):split_size*(i+2)]
            if len(test) == 0:
                break
            # 這裡可結合optimizer進行訓練集優化
            # 測試集回測
            results.append({'train_len': len(train), 'test_len': len(test)})
        return results
