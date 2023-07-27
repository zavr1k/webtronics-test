import os

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
JWT_SECRET = os.getenv("JWT_SECRET", "SECRET")
USER_MANAGER_SECRET = os.getenv("USER_MANAGER_SECRET", "SECRET")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

FETCH_LIMIT = 10
