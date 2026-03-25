import os
import re
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the same directory as this file (next to app.py)
load_dotenv(Path(__file__).resolve().parent / ".env")


def _env_bool(name: str, default: bool) -> bool:
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_ENDPOINT = os.environ.get("API_ENDPOINT")
    HISTORYAPI_ENDPOINT = os.environ.get("HISTORYAPI_ENDPOINT")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = 900  # 900 seconds = 15 minutes

    WHITELIST_PATTERN = re.compile(r"^[a-zA-Z0-9@._-]+$")

    SESSION_COOKIE_HTTPONLY = _env_bool("SESSION_COOKIE_HTTPONLY", True)
    SESSION_COOKIE_SECURE = _env_bool("SESSION_COOKIE_SECURE", True)
