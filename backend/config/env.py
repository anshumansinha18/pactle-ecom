from dotenv import load_dotenv
from pathlib import Path
import os


# Load the appropriate .env file once when this module is imported
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_DIR = BASE_DIR / "env"
ENV_FILE = os.getenv("ENV_FILE", ".env.dev")
load_dotenv(dotenv_path=ENV_DIR / ENV_FILE)

def get_current_env_value(key: str) -> str:
     value = os.getenv(key)
     if value is None:
        raise RuntimeError(f"Key not present in environment variable: {key}")
     return value

def get_optional_env_value(key: str, default=None):
    return os.getenv(key, default)