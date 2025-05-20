from setuptools import setup, find_packages

setup(
    name='CryptoQuantFactory',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas', 'numpy', 'matplotlib', 'optuna', 'ccxt', 'yfinance', 'requests', 'streamlit', 'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'cqf-cli=interface.cli:main',
        ],
    },
    author='Your Name',
    description='A multi-strategy crypto quant backtest platform',
    url='https://github.com/yourname/cryptoquantfactory',
)
