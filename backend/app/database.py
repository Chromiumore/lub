from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_config, Config

def get_db(config: Annotated[Config, Depends(get_config)]):
    DATABASE_URL = config.db.get_db_url()
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[Session, Depends(get_db)]
