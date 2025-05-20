import sys

MIN_VERSION = (3, 8)
MAX_VERSION = (3, 12)

if not (MIN_VERSION <= sys.version_info[:2] <= MAX_VERSION):
    print(f"Python {MIN_VERSION[0]}.{MIN_VERSION[1]} to {MAX_VERSION[0]}.{MAX_VERSION[1]} supported. Current: {sys.version}")
    sys.exit(1)
else:
    print(f"Python version {sys.version_info[0]}.{sys.version_info[1]} OK.")
