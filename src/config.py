from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    POSTGRES_DB: str = "webtronics"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_USER: str = "anton"
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    JWT_SECRET: str = "SECRET"
    USER_MANAGER_SECRET_RESET: str = "SECRET"
    USER_MANAGER_SECRET_VERIFY: str = "SECRET"

    FETCH_LIMIT: int = 10

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


settings = Settings()
