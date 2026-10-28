"""Repository paths shared by the figure and table scripts."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = os.environ.get('PENSIMOPT_DATA', os.path.relpath(ROOT / 'data')) + '/'
OUTD = os.environ.get('PENSIMOPT_OUT', os.path.relpath(ROOT / 'output')) + '/'
os.makedirs(OUTD, exist_ok=True)
