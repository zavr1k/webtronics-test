import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB", "webtronics")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_USER = os.getenv("POSTGRES_USER", "anton")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

JWT_SECRET = os.getenv("JWT_SECRET", "SECRET")
USER_MANAGER_SECRET_RESET = os.getenv("USER_MANAGER_SECRET_RESET", "SECRET")
USER_MANAGER_SECRET_VERIFY = os.getenv("USER_MANAGER_SECRET_VERIFY", "SECRET")

FETCH_LIMIT = 10
