import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB", "webtronics")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

JWT_SECRET = os.getenv("JWT_SECRET", "SECRET")
USER_MANAGER_SECRET_RESET = os.getenv("USER_MANAGER_SECRET_RESET", "SECRET")
USER_MANAGER_SECRET_VERIFY = os.getenv("USER_MANAGER_SECRET_VERIFY", "SECRET")

FETCH_LIMIT = 10
