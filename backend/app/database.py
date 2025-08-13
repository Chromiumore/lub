from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config

config = Config.load()


class DatabaseHelper:
    def __init__(self, url: str):
        self.engine = create_engine(url)
        self.session_maker = sessionmaker(bind=self.engine)


db_helper = DatabaseHelper(
    config.db.get_db_url(),
)
