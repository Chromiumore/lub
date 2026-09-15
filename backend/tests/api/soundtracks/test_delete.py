from app.main import API_V1_PREFIX
from app.files.storage import BUCKET_NAME
from app.models import File, Soundtrack, User


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


def test_delete_not_exists(client):
    response = client.delete(API_V1_PREFIX + '/music/123/')
    
    assert response.status_code == 404
