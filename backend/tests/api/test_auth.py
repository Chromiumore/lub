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

def test_register_bad_email(client, db_session):
    username = str(uuid4())
    password = '12345'
    email = f'{username}@badmail'
    payload = {
        'username': username,
        'password': password,
        'email': email
        }
    response = client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 422
    assert response.json().get('detail')[0].get('type') == 'value_error'

    user = db_session.query(User).filter_by(username=username).first()
    assert user is None

def test_login_success(client, default_user):
    payload = {
        'email': default_user.email,
        'password': default_user.password.get_secret_value()
    }

    response = client.post(API_V1_PREFIX + '/login', json=payload)

    assert response.status_code == 200
    assert type(response.json().get('access_token')) is str
    assert type(response.json().get('refresh_token')) is str

def test_login_not_exists(client, default_user):
    payload = {
        'email': 'johndoe@mail.com',
        'password': 'iamnewuser'
    }

    response = client.post(API_V1_PREFIX + '/login', json=payload)

    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect email or password'

def test_login_wrong_password(client, default_user):
    payload = {
        'email': default_user.email,
        'password': default_user.password.get_secret_value() + '123123'
    }

    response = client.post(API_V1_PREFIX + '/login', json=payload)

    assert response.status_code == 401
    assert response.json().get('detail') == 'Incorrect email or password'
