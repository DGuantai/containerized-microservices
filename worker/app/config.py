from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = "jobsdb"
    db_user: str = "jobsuser"
    db_password: str = "change_me"

    redis_host: str = "redis"
    redis_port: int = 6379

    worker_poll_seconds: int = 2
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file="compose/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


settings = Settings()