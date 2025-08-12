from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import Config

config = Config.load()

class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.session_maker = sessionmaker(bind=self.engine)

DATABASE_URL = f'postgresql+psycopg2://{config.db.user}:{config.db.password.get_secret_value()}@{config.db.host}:{config.db.port}/{config.db.name}'

db_helper = DatabaseHelper(
    DATABASE_URL,
)
