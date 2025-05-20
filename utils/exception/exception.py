class CryptoQuantFactoryError(Exception):
    """Base exception for CryptoQuantFactory"""
    pass

class DataSourceError(CryptoQuantFactoryError):
    pass

class StrategyError(CryptoQuantFactoryError):
    pass

class BacktestError(CryptoQuantFactoryError):
    pass

class TradingError(CryptoQuantFactoryError):
    pass
