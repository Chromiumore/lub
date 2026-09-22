import io

import pytest
import pytest_asyncio
from fastapi import UploadFile
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from minio import Minio
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

@pytest_asyncio.fixture(scope='session', loop_scope='session')
async def db_engine(app_config):
    engine = create_async_engine(app_config.db.get_db_url())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope='session', loop_scope='session')
async def db_session_factory(db_engine):
    return async_sessionmaker(autocommit=False, autoflush=False, bind=db_engine, expire_on_commit=False, class_=AsyncSession)

@pytest_asyncio.fixture(loop_scope='session')
async def db_session(db_session_factory):
    async with db_session_factory() as session:
        yield session
        await session.rollback()

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


@pytest_asyncio.fixture
async def client(db_session, app_config, minio_client):

    async def _get_test_db():
        yield db_session
        await db_session.flush()

    def _get_test_config():
        return app_config

    def _get_test_minio_client():
        return minio_client

    app = create_app()

    app.dependency_overrides[get_db] = _get_test_db
    app.dependency_overrides[get_config] = _get_test_config
    app.dependency_overrides[get_minio_client] = _get_test_minio_client

    transport = ASGITransport(app=app)
    async with AsyncClient(base_url='http://localhost:8000', transport=transport) as ac:
        yield ac

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

@pytest.fixture(scope='session')
def media_bytes(request, empty_mp3_bytes, empty_jpeg_bytes):
    file_type = request.param
    if file_type == FileType.sound:
        return empty_mp3_bytes
    elif file_type == FileType.image:
        return empty_jpeg_bytes

@pytest_asyncio.fixture
async def default_user(db_session):
    creds = RegisterSchema(
                username='user123',
                password='12345',
                email='user@gmail.com'
            )

    users_repo = UsersRepository(db_session)
    user = await users_repo.add(creds)

    return user.id, creds


@pytest_asyncio.fixture
async def default_track(db_session, default_user, files_service, empty_mp3_bytes, empty_jpeg_bytes):
    db_track = Soundtrack(name='track-1', author_id = default_user[0])
    db_session.add(db_track)
    await db_session.flush()
    await files_service.upload_audio(UploadFile(file=io.BytesIO(empty_mp3_bytes[0]), filename=empty_mp3_bytes[1]), db_track)
    await files_service.upload_cover(UploadFile(file=io.BytesIO(empty_jpeg_bytes[0]), filename=empty_jpeg_bytes[1]), db_track)
    tracks_repo = SoundtracksRepository(db_session)
    db_track = await tracks_repo.get_by_id(db_track.id)
    return db_track
