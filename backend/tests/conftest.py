import io

import pytest
import pytest_asyncio
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from minio import Minio
from minio.deleteobjects import DeleteObject
from dotenv import load_dotenv

from app.main import create_app
from app.models import Base
from app.config import Config, get_config
from app.database import get_db
from app.models import Soundtrack, File, FileType
from app.soundtracks.repository import SoundtracksRepository
from app.files.minio import get_minio_client
from app.files.repository import FilesRepository
from app.files.service import FilesService
from app.files.storage import FileStorage, BUCKET_NAME
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
    minio = Minio(
        endpoint=minio_config.endpoint,
        access_key=minio_config.user,
        secret_key=minio_config.password.get_secret_value(),
        secure=False
    )

    if not minio.bucket_exists(BUCKET_NAME):
        minio.make_bucket(BUCKET_NAME)

    yield minio

    objects_to_delete = minio.list_objects(BUCKET_NAME, recursive=True)
    for obj in objects_to_delete:
        minio.remove_object(BUCKET_NAME, obj.object_name)
    
    minio.remove_bucket(BUCKET_NAME)


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


# SERVICES AND REPOSITORIES

@pytest.fixture
def files_service(db_session, minio_client):
    return FilesService(
        FilesRepository(db_session),
        SoundtracksRepository(db_session),
        FileStorage(minio_client)
    )


# DTOs, ENTITIES AND TEST DATA

@pytest.fixture(scope='session')
def empty_mp3_bytes(pytestconfig):
    filename = 'silence.mp3'
    with open(pytestconfig.rootpath / 'tests' / 'fixtures' / filename, 'rb') as f:
        return f.read(), filename

@pytest.fixture(scope='session')
def empty_jpeg_bytes():
    filename = 'image.jpg'
    return b'fake', filename
    

@pytest.fixture
def default_user(db_session):
    creds = RegisterSchema(
                username='user123',
                password='12345',
                email='user@gmail.com'
            )

    users_repo = UsersRepository(db_session)
    user = users_repo.add(creds)

    return user.id, creds


@pytest_asyncio.fixture
async def default_track(db_session, default_user, files_service, empty_mp3_bytes, empty_jpeg_bytes):
    db_track = Soundtrack(name='track-1', author_id = default_user[0])
    db_session.add(db_track)
    db_session.commit()
    db_session.refresh(db_track)
    await files_service.upload_audio(UploadFile(file=io.BytesIO(empty_mp3_bytes[0]), filename=empty_mp3_bytes[1]), db_track)
    files_service.upload_cover(UploadFile(file=io.BytesIO(empty_jpeg_bytes[0]), filename=empty_jpeg_bytes[1]), db_track)
    return db_track
