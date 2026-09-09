import json
from io import BytesIO

import pytest

from app.main import API_V1_PREFIX
from app.files.storage import BUCKET_NAME
from app.models import File, FileType, Soundtrack, User


def test_create_track(client, db_session, minio_client, default_user, empty_mp3_bytes, empty_jpeg_bytes):
    track_data = {
        'name': 'track1234',
        'author_id': default_user[0]
    }

    
    audio_file = (empty_mp3_bytes[1], BytesIO(empty_mp3_bytes[0]), 'audio/mpeg')
    cover_file = (empty_jpeg_bytes[1], BytesIO(empty_jpeg_bytes[0]), 'image/jpeg')

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


def test_get_track(client, default_track):
    response = client.get(API_V1_PREFIX + f'/music/{default_track.id}')
    assert response.status_code == 200

    result = response.json()
    assert result.get('id') == default_track.id
    assert result.get('name') == default_track.name
    assert result.get('author').get('id') == default_track.author.id
    assert result.get('author').get('username') == default_track.author.username

    files_result = result.get('files')
    assert any(f.get('file_type') == FileType.image.value and f.get('duration') is None for f in files_result)
    assert any(f.get('file_type') == FileType.sound.value and f.get('duration') for f in files_result)


def test_get_tracks(client, default_track):
    response = client.get(API_V1_PREFIX + '/music')
    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 1

    track = result[0]
    assert track.get('id') == default_track.id
    assert track.get('author')
    assert len(track.get('files')) == 2


def test_update_track(client, default_track, db_session):
    new_name = 'update-track'
    payload = {'name': new_name}
    response = client.put(API_V1_PREFIX + f'/music/{default_track.id}', json=payload)
    assert response.status_code == 200

    result = response.json()
    assert result.get('id') == default_track.id
    assert result.get('name') == new_name
    assert result.get('author').get('id') == default_track.author.id
    assert result.get('author').get('username') == default_track.author.username

    assert len(result.get('files')) == 2

    db_track = db_session.query(Soundtrack).filter_by(id=default_track.id).first()
    assert db_track.name == new_name

def test_delete_track(client, default_track, db_session, minio_client):
    db_files = db_session.query(File).filter_by(soundtrack_id=default_track.id).all()
    assert len(db_files) == 2

    response = client.delete(API_V1_PREFIX + f'/music/{default_track.id}/')

    assert response.status_code == 200

    db_track = db_session.query(Soundtrack).filter_by(id=default_track.id).first()

    assert not db_track

    assert len(list(minio_client.list_objects(BUCKET_NAME))) == 0

    db_files = db_session.query(File).filter_by(soundtrack_id=default_track.id).all()
    assert len(db_files) == 0

    assert db_session.query(User).filter_by(id=default_track.author.id).first()
    