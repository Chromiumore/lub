import time

import json
from io import BytesIO

from app.main import API_V1_PREFIX
from app.files.storage import BUCKET_NAME
from app.models import File, FileType, Soundtrack


def test_create_track(client, db_session, minio_client, default_user, empty_mp3_bytes):
    track_data = {
        'name': 'track1234',
        'author_id': default_user[0]
    }

    
    audio_file = ('song.mp3', BytesIO(empty_mp3_bytes), 'audio/mpeg')

    cover_content = b'fake image data'
    cover_file = ('cover.jpg', BytesIO(cover_content), 'image/jpeg')

    response = client.post(
        API_V1_PREFIX + '/music/',
        files={
            'audio_file': audio_file,
            'cover_image': cover_file
        },
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
    assert len(files_result) == 2
    assert any(f.get('file_type') == FileType.image.value and f.get('duration') is None for f in files_result)
    assert any(f.get('file_type') == FileType.sound.value and f.get('duration') for f in files_result)

    id = result.get('id')
    assert id

    db_track = db_session.query(Soundtrack).filter_by(id=id).first()
    assert db_track

    db_files = db_session.query(File).filter_by(soundtrack_id=id).all()
    assert len(db_files) == 2

    assert minio_client.get_object(BUCKET_NAME, db_files[0].storage_filename)
    assert minio_client.get_object(BUCKET_NAME, db_files[1].storage_filename)
    