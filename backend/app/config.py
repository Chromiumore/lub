from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

    
class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='db_', case_sensitive=False)

    host: str
    name: str
    user: str
    password: SecretStr

    def get_db_url(self):
        return (f'postgresql+psycopg2://'
                f'{self.user}:{self.password.get_secret_value()}@{self.host}:5432/{self.name}')


class S3Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='s3_', case_sensitive=False)

    endpoint: str
    user: str
    password: SecretStr


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='auth_', case_sensitive=False)

    secret_key: SecretStr


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    s3: S3Config = Field(default_factory=S3Config)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    model_config = SettingsConfigDict(
            env_file='.env',
            extra='ignore',
        )


@lru_cache
def get_config() -> Config:
    return Config()
