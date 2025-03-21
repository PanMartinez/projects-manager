from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    allowed_hosts: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    model_config = SettingsConfigDict(
        env_file="projects_manager/config/.env", env_file_encoding="utf-8"
    )

    @property
    def database_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{int(self.db_port)}/{self.db_name}"


@lru_cache
def get_settings():
    return Settings()
