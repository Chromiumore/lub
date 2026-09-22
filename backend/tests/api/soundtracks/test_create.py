import json
from io import BytesIO

import pytest
from pytest_lazy_fixtures import lf
from sqlalchemy import select

from app.main import API_V1_PREFIX
from app.files.storage import BUCKET_NAME
from app.models import File, FileType, Soundtrack


async def test_create_track(client, db_session, minio_client, default_user, empty_mp3_bytes, empty_jpeg_bytes):
    track_data = {
        'name': 'track1234',
        'author_id': default_user[0]
    }
    audio_file = (empty_mp3_bytes[1], BytesIO(empty_mp3_bytes[0]), 'audio/mpeg')
    cover_file = (empty_jpeg_bytes[1], BytesIO(empty_jpeg_bytes[0]), 'image/jpeg')

    files = {
        'audio_file': audio_file,
        'cover_image': cover_file
    }

    response = await client.post(
        API_V1_PREFIX + '/music/',
        files=files,
        data = {
            'track': json.dumps(track_data)
        }
    )

    assert response.status_code == 201
    result = response.json()

    assert result.get('name') == track_data['name']
    assert result.get('author').get('id') == default_user[0]
    assert result.get('author').get('username') == default_user[1].username

    files_result = result.get('files')
    assert len(files_result) == len(files)
    assert any(f.get('file_type') == FileType.sound.value and f.get('duration') is not None for f in files_result)
    assert any(f.get('file_type') == FileType.image.value and f.get('duration') is None for f in files_result)

    id = result.get('id')
    assert id

    db_track = await db_session.get(Soundtrack, id)
    assert db_track

    db_files = (await db_session.execute(select(File).filter_by(soundtrack_id=id))).scalars().all()
    assert len(db_files) == len(files)

    assert minio_client.get_object(BUCKET_NAME, next(f.storage_filename for f in db_files if f.file_type == FileType.sound))
    assert minio_client.get_object(BUCKET_NAME, next(f.storage_filename for f in db_files if f.file_type == FileType.image))
    