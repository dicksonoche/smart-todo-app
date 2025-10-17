import os
import sys

# Ensure 'src' is on sys.path so 'utils' is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.logger import silence_third_party_warnings