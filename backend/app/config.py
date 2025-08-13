from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
    )


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='db_', case_sensitive=False)

    host: str
    port: str
    name: str
    user: str
    password: SecretStr

    def get_db_url(self):
        return (f'postgresql+psycopg2://'
                f'{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}')


class Config(BaseSettings):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()
