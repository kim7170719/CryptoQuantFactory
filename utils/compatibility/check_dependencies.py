import pkg_resources
import sys

REQUIRED = [
    'pandas', 'numpy', 'matplotlib', 'optuna', 'ccxt', 'yfinance', 'requests', 'streamlit', 'scikit-learn', 'memory_profiler', 'pytest', 'pytest-cov', 'cryptography'
]

def check_dependencies():
    missing = []
    for pkg in REQUIRED:
        try:
            pkg_resources.get_distribution(pkg)
        except pkg_resources.DistributionNotFound:
            missing.append(pkg)
    if missing:
        print(f'Missing packages: {missing}')
        sys.exit(1)
    print('All dependencies satisfied.')

if __name__ == '__main__':
    check_dependencies()
