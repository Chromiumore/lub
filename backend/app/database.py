from sqlalchemy import create_engine
from .config import Config

config = Config.load()

db_name = config.db.name
db_user = config.db.user
db_pass = config.db.password
db_host = config.db.host
db_port = config.db.port

db_engine = create_engine(f'postgresql+psycopg2://{db_user}:{12345}@{db_host}:{db_port}/{db_name}')
