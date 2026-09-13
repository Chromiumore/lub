from io import BytesIO

import pytest

from app.main import API_V1_PREFIX
from app.models import File, FileType, Soundtrack, User
from app.files.storage import BUCKET_NAME


@pytest.mark.parametrize(
    'file_fixture, path_segment',
    [
        ('empty_mp3_bytes', 'file'),
        ('empty_jpeg_bytes', 'cover')
    ]
)
def test_donwload(request, client, default_track, file_fixture, path_segment):
    empty_bytes = request.getfixturevalue(file_fixture)
    file_content, filename = empty_bytes

    response = client.get(API_V1_PREFIX + f'/music/{default_track.id}/{path_segment}')
    assert response.status_code == 200
    assert response.headers['content-disposition'] == f'attachment; filename="{filename}"'
    assert response.content == file_content


@pytest.mark.parametrize(
    'file_fixture, path_segment',
    [
        ('empty_mp3_bytes', 'file'),
        ('empty_jpeg_bytes', 'cover')
    ]
)
def test_download_not_exists(request, client, default_track, file_fixture, path_segment):
    empty_bytes = request.getfixturevalue(file_fixture)
    file_content, filename = empty_bytes

    response = client.get(API_V1_PREFIX + f'/music/{default_track.id + 11}/file')
    assert response.status_code == 404
    assert not response.headers.get('content-disposition')
    assert not response.content


@pytest.mark.parametrize(
    'path_segment, file_type',
    [
        ('file', FileType.sound),
        ('cover', FileType.image)
    ]
)
def test_update(client, default_track, pytestconfig, minio_client, db_session, path_segment, file_type):
    if file_type == FileType.sound:
        new_filename = 'silence2.mp3'
        with open(pytestconfig.rootpath / 'tests' / 'fixtures' / new_filename, 'rb') as f:
            content = f.read()
    else:
        new_filename = 'new_cover2_update.jpg'
        content = b'new fake bytes new fake bytes'

    file = (new_filename, BytesIO(content), 'audio/mpeg' if file_type == FileType.sound else 'image/jpeg')

    response = client.put(
        API_V1_PREFIX + f'/music/{default_track.id}/{path_segment}',
        files={
            'file': file
        }
    )

    assert response.status_code == 200

    db_file = db_session.query(File).filter_by(soundtrack_id=default_track.id, file_type=file_type).first()
    assert db_file.original_filename == new_filename

    assert minio_client.get_object(BUCKET_NAME, db_file.storage_filename).read() == content


@pytest.mark.parametrize(
    'file_fixture, path_segment, file_type',
    [
        ('empty_mp3_bytes', 'file', FileType.sound),
        ('empty_jpeg_bytes', 'cover', FileType.image)
    ]
)
def test_update_not_exists(request, client, default_track, db_session, minio_client, file_fixture, path_segment, file_type, pytestconfig):
    empty_bytes = request.getfixturevalue(file_fixture)
    old_content, old_filename = empty_bytes
    if file_type == FileType.sound:
        new_filename = 'silence2.mp3'
        with open(pytestconfig.rootpath / 'tests' / 'fixtures' / new_filename, 'rb') as f:
            new_content = f.read()
    else:
        new_filename = 'new_cover2_update.jpg'
        new_content = b'new fake bytes new fake bytes'

    file = (new_filename, BytesIO(new_content), 'audio/mpeg' if file_type == FileType.sound else 'image/jpeg')

    response = client.put(
        API_V1_PREFIX + f'/music/{default_track.id + 11}/{path_segment}',
        files={
            'file': file
        }
    )

    assert response.status_code == 404

    db_file = db_session.query(File).filter_by(soundtrack_id=default_track.id, file_type=file_type).first()
    assert db_file.original_filename == old_filename

    assert minio_client.get_object(BUCKET_NAME, db_file.storage_filename).read() == old_content
