from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    name: str = "chat-with-news"
    env: str = Field("dev", env="ENV")
    db_conn: str = Field(...)


settings = Settings()
