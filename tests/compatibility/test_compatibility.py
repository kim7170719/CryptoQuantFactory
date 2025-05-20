import sys
import subprocess

def test_python_version():
    result = subprocess.run([sys.executable, 'utils/compatibility/python_version_check.py'], capture_output=True, text=True)
    assert 'OK' in result.stdout

def test_dependencies():
    result = subprocess.run([sys.executable, 'utils/compatibility/check_dependencies.py'], capture_output=True, text=True)
    assert 'All dependencies satisfied.' in result.stdout
