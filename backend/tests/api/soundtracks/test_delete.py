from sqlalchemy import select

from app.main import API_V1_PREFIX
from app.files.storage import BUCKET_NAME
from app.models import File, Soundtrack, User


async def test_delete_track(client, default_track, db_session, minio_client):
    db_files = (await db_session.execute(select(File).filter_by(soundtrack_id=default_track.id))).scalars().all()
    assert len(db_files) == 2

    response = await client.delete(API_V1_PREFIX + f'/music/{default_track.id}/')

    assert response.status_code == 200

    db_track = await db_session.get(Soundtrack, default_track.id)

    assert not db_track

    assert len(list(minio_client.list_objects(BUCKET_NAME))) == 0

    db_files = (await db_session.execute(select(File).filter_by(soundtrack_id=default_track.id))).scalars().all()
    assert len(db_files) == 0

    assert (await db_session.execute(select(User).filter_by(id=default_track.author.id))).scalar_one_or_none()


async def test_delete_not_exists(client):
    response = await client.delete(API_V1_PREFIX + '/music/123/')
    
    assert response.status_code == 404
