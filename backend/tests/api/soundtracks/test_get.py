from app.main import API_V1_PREFIX
from app.models import FileType


async def test_get_track(client, default_track):
    response = await client.get(API_V1_PREFIX + f'/music/{default_track.id}')
    assert response.status_code == 200

    result = response.json()
    assert result.get('id') == default_track.id
    assert result.get('name') == default_track.name
    assert result.get('author').get('id') == default_track.author.id
    assert result.get('author').get('username') == default_track.author.username

    files_result = result.get('files')
    assert any(f.get('file_type') == FileType.cover.value and f.get('duration') is None for f in files_result)
    assert any(f.get('file_type') == FileType.audio.value and f.get('duration') is not None for f in files_result)


async def test_get_tracks(client, default_track):
    response = await client.get(API_V1_PREFIX + '/music')
    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 1

    track = result[0]
    assert track.get('id') == default_track.id
    assert track.get('author')
    assert len(track.get('files')) == 2
