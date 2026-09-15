import json
from io import BytesIO

import pytest
from pytest_lazy_fixtures import lf

from app.main import API_V1_PREFIX
from app.files.storage import BUCKET_NAME
from app.models import File, FileType, Soundtrack


@pytest.mark.parametrize(
    'created_track, jpeg_bytes',
    [
        (None, None),
        (lf('default_track'), lf('empty_jpeg_bytes'))
    ]
)
def test_create_track(client, db_session, minio_client, default_user, empty_mp3_bytes, jpeg_bytes, created_track):
    track_data = {
        'name': 'track1234' if not created_track else created_track.name,
        'author_id': default_user[0]
    }
    audio_file = (empty_mp3_bytes[1], BytesIO(empty_mp3_bytes[0]), 'audio/mpeg')

    files = {
        'audio_file': audio_file,
    }

    # If image file is attached
    if jpeg_bytes:
        cover_file = (jpeg_bytes[1], BytesIO(jpeg_bytes[0]), 'image/jpeg')
        files['cover_image'] = cover_file

    response = client.post(
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
    assert any(f.get('file_type') == FileType.sound.value and f.get('duration') for f in files_result)

    id = result.get('id')
    assert id

    db_track = db_session.query(Soundtrack).filter_by(id=id).first()
    assert db_track

    db_files = db_session.query(File).filter_by(soundtrack_id=id).all()
    assert len(db_files) == len(files)

    assert minio_client.get_object(BUCKET_NAME, next(f.storage_filename for f in db_files if f.file_type == FileType.sound))

    # If image file is attached
    if jpeg_bytes:
        assert any(f.get('file_type') == FileType.image.value and f.get('duration') is None for f in files_result)
        assert minio_client.get_object(BUCKET_NAME, next(f.storage_filename for f in db_files if f.file_type == FileType.image))
    