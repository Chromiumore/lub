from app.main import API_V1_PREFIX
from app.models import Soundtrack


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
