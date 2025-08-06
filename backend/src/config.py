from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='backend/.env',
    )


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='db_', case_sensitive=False)

    host: str
    port: str
    name: str
    user: str
    password: SecretStr


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
