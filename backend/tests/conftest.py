import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from minio import Minio
from dotenv import load_dotenv

from app.main import create_app
from app.models import Base
from app.config import Config, get_config
from app.database import get_db
from app.files.minio import get_minio_client
from app.auth.repository import UsersRepository
from app.auth.schemas import RegisterSchema


TEST_ENV_FILE = '.env.test'


# MAIN FIXTURES

@pytest.fixture(scope='session')
def app_config():
    load_dotenv(TEST_ENV_FILE)

    return Config()

@pytest.fixture
def db_session(app_config):
    test_database_url = app_config.db.get_db_url()
    engine = create_engine(test_database_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def minio_client(app_config):
    minio_config = app_config.s3
    return Minio(
        endpoint=minio_config.endpoint,
        access_key=minio_config.user,
        secret_key=minio_config.password.get_secret_value(),
        secure=False
    )

@pytest.fixture
def client(db_session, app_config, minio_client):

    def _get_test_db():
        return db_session

    def _get_test_config():
        return app_config

    def _get_test_minio_client():
        return minio_client

    app = create_app()

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_config] = _get_test_config
    app.dependency_overrides[get_minio_client] = _get_test_minio_client

    with TestClient(app) as c:  
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def default_user(db_session):
    creds = RegisterSchema(
                username='user123',
                password='12345',
                email='user@gmail.com'
            )

    users_repo = UsersRepository(db_session)
    users_repo.add(creds)

    return creds
