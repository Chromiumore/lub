from io import BytesIO

import pytest
from sqlalchemy import select

from app.main import API_V1_PREFIX
from app.models import File, FileType
from app.files.storage import BUCKET_NAME


@pytest.mark.parametrize(
    'media_bytes, path_segment',
    [
        (FileType.audio, 'file'),
        (FileType.cover, 'cover')
    ],
    indirect=['media_bytes']
)
async def test_download(client, default_track, media_bytes, path_segment):
    file_content, filename = media_bytes

    response = await client.get(API_V1_PREFIX + f'/music/{default_track.id}/{path_segment}')
    assert response.status_code == 200
    assert response.headers['content-disposition'] == f'attachment; filename="{filename}"'
    assert response.content == file_content


@pytest.mark.parametrize(
    'media_bytes, path_segment',
    [
        (FileType.audio, 'file'),
        (FileType.cover, 'cover')
    ],
    indirect=['media_bytes']
)
async def test_download_not_exists(client, default_track, media_bytes, path_segment):
    file_content, filename = media_bytes

    response = await client.get(API_V1_PREFIX + f'/music/{default_track.id + 11}/{path_segment}')
    assert response.status_code == 404
    assert not response.headers.get('content-disposition')
    assert not response.content


@pytest.mark.parametrize(
    'path_segment, file_type',
    [
        ('file', FileType.audio),
        ('cover', FileType.cover)
    ]
)
async def test_update(client, default_track, pytestconfig, minio_client, db_session, path_segment, file_type):
    if file_type == FileType.audio:
        new_filename = 'silence2.mp3'
        with open(pytestconfig.rootpath / 'tests' / 'fixtures' / new_filename, 'rb') as f:
            content = f.read()
    else:
        new_filename = 'new_cover2_update.jpg'
        content = b'new fake bytes new fake bytes'

    file = (new_filename, BytesIO(content), 'audio/mpeg' if file_type == FileType.audio else 'image/jpeg')

    response = await client.put(
        API_V1_PREFIX + f'/music/{default_track.id}/{path_segment}',
        files={
            'file': file
        }
    )

    assert response.status_code == 200

    db_file = (await db_session.execute(select(File).filter_by(soundtrack_id=default_track.id, file_type=file_type))).scalar_one_or_none()
    assert db_file.original_filename == new_filename

    assert minio_client.get_object(BUCKET_NAME, db_file.storage_filename).read() == content


@pytest.mark.parametrize(
    'media_bytes, file_type, path_segment',
    [
        (FileType.audio, FileType.audio, 'file'),
        (FileType.cover, FileType.cover, 'cover')
    ],
    indirect=['media_bytes']
)
async def test_update_not_exists(client, default_track, db_session, minio_client, media_bytes, path_segment, file_type, pytestconfig):
    old_content, old_filename = media_bytes
    if file_type == FileType.audio:
        new_filename = 'silence2.mp3'
        with open(pytestconfig.rootpath / 'tests' / 'fixtures' / new_filename, 'rb') as f:
            new_content = f.read()
    else:
        new_filename = 'new_cover2_update.jpg'
        new_content = b'new fake bytes new fake bytes'

    file = (new_filename, BytesIO(new_content), 'audio/mpeg' if file_type == FileType.audio else 'image/jpeg')

    response = await client.put(
        API_V1_PREFIX + f'/music/{default_track.id + 11}/{path_segment}',
        files={
            'file': file
        }
    )

    assert response.status_code == 404

    db_file = (await db_session.execute(select(File).filter_by(soundtrack_id=default_track.id, file_type=file_type))).scalar_one_or_none()
    assert db_file.original_filename == old_filename

    assert minio_client.get_object(BUCKET_NAME, db_file.storage_filename).read() == old_content
