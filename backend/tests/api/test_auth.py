from uuid import uuid4
from hashlib import sha256

from app.main import API_V1_PREFIX
from app.models import User


def test_register_success(client, db_session):
    username = str(uuid4())
    password = '12345'
    email = f'{username}@gmail.com'
    payload = {
        'username': username,
        'password': password,
        'email': email
        }
    response = client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 201

    created_user = db_session.query(User).filter_by(email=email, password_hash=sha256(password.encode('utf-8')).hexdigest()).first()

    assert created_user is not None
    assert created_user.email == email
    assert created_user.username == username
    assert created_user.password_hash == sha256(password.encode('utf-8')).hexdigest()
