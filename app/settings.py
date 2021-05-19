import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


TINKOFF_SANDBOX_TOKEN = os.getenv("TINKOFF_SANDBOX_TOKEN")
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_DIR = ROOT_DIR / "data"
