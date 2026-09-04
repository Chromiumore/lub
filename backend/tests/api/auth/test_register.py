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

def test_regiser_password_exists(client, default_user, db_session):
    payload = {
            'username': default_user.username + 'new',
            'password': default_user.password.get_secret_value(),
            'email': 'new_email_' + default_user.email
            }
    response = client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 201
    created_user = db_session.query(User).filter_by(email=payload['email'], password_hash=sha256(payload['password'].encode('utf-8')).hexdigest()).first()

    assert created_user is not None
    assert created_user.email == payload['email']

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

def test_register_no_required_fields(client):
    payload = {
            'username': 'abc',
            'password': 'password',
            }
    response = client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 422

def test_register_username_already_exists(client, default_user):
    payload = {
            'username': default_user.username,
            'password': 'pass123',
            'email': 'abc_' + default_user.email
            }
    response = client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 409
    assert response.json().get('detail') == 'A user with this username already exists.'

def test_register_email_already_exists(client, default_user):
    payload = {
                'username': default_user.username + 'new',
                'password': 'pass123',
                'email': default_user.email
                }
    response = client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 409
    assert response.json().get('detail') == 'A user with this email address already exists.'
    