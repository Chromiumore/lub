from io import BytesIO

from app.main import API_V1_PREFIX
from app.models import File, FileType, Soundtrack, User
from app.files.storage import BUCKET_NAME


def test_donwload_audio(client, default_track, empty_mp3_bytes):
    file_content, filename = empty_mp3_bytes

    response = client.get(API_V1_PREFIX + f'/music/{default_track.id}/file')
    assert response.status_code == 200
    assert response.headers['content-disposition'] == f'attachment; filename="{filename}"'
    assert response.content == file_content


def test_download_audio_not_exists(client, default_track, empty_mp3_bytes):
    file_content, filename = empty_mp3_bytes

    response = client.get(API_V1_PREFIX + f'/music/{default_track.id + 11}/file')
    assert response.status_code == 404
    assert not response.headers.get('content-disposition')
    assert not response.content


def test_update_audio(client, default_track, pytestconfig, minio_client, db_session):
    new_filename = 'silence2.mp3'
    with open(pytestconfig.rootpath / 'tests' / 'fixtures' / new_filename, 'rb') as f:
        content = f.read()

    audio_file = (new_filename, BytesIO(content), 'audio/mpeg')

    response = client.put(
        API_V1_PREFIX + f'/music/{default_track.id}/file',
        files={
            'file': audio_file
        }
    )

    assert response.status_code == 200

    db_file = db_session.query(File).filter_by(soundtrack_id=default_track.id, file_type=FileType.sound).first()
    assert db_file.original_filename == new_filename

    assert minio_client.get_object(BUCKET_NAME, db_file.storage_filename).read() == content 
    