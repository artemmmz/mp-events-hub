from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class PgSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    db: str = Field(default="events-hub", alias="PG__DB")
    user: str = Field(default="admin", alias="PG__USER")
    password: str = Field(default="admin", alias="PG__PASSWORD")
    host: str = Field(default="events-hub", alias="PG__HOST")
    port: str = Field(default="5432", alias="PG__PORT")

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    secret_key: str = Field(default="", alias="AUTH__SECRET_KEY")
    access_token_lifetime: int = Field(default=5_000_000_000, alias="AUTH__ACCESS_TOKEN_LIFETIME")
    algorithm: str = Field(default="sha256", alias="AUTH__ALGORITHM")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".dev.env"),
        extra="ignore",
    )

    pg: PgSettings = PgSettings()
    auth: AuthSettings = AuthSettings()


def get_settings() -> Settings:
    return Settings()