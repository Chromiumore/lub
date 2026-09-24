from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='db_',
        case_sensitive=False,
        extra='ignore',
    )

    endpoint: str
    name: str
    user: str
    password: SecretStr

    def get_sync_db_url(self):
        return (f'postgresql+psycopg2://'
                f'{self.user}:{self.password.get_secret_value()}@{self.endpoint}/{self.name}')

    def get_async_db_url(self):
        return (f'postgresql+asyncpg://'
                f'{self.user}:{self.password.get_secret_value()}@{self.endpoint}/{self.name}')


class S3Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='s3_',
        case_sensitive=False,
        extra='ignore',
    )

    endpoint: str
    user: str
    password: SecretStr


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='auth_',
        case_sensitive=False,
        extra='ignore',
    )

    secret_key: SecretStr


class Config(BaseSettings):    
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    s3: S3Config = Field(default_factory=S3Config)
    auth: AuthConfig = Field(default_factory=AuthConfig)


@lru_cache
def get_config() -> Config:
    return Config()
