from uuid import uuid4
from hashlib import sha256

from sqlalchemy import select

from app.main import API_V1_PREFIX
from app.models import User


async def test_register_success(client, db_session):
    username = str(uuid4())
    password = '12345'
    email = f'{username}@gmail.com'
    payload = {
        'username': username,
        'password': password,
        'email': email
        }
    response = await client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 201

    created_user = (await db_session.execute(select(User).filter_by(email=email, password_hash=sha256(password.encode('utf-8')).hexdigest()))).scalar_one_or_none()

    assert created_user is not None
    assert created_user.email == email
    assert created_user.username == username
    assert created_user.password_hash == sha256(password.encode('utf-8')).hexdigest()

async def test_regiser_password_exists(client, default_user, db_session):
    user_data = default_user[1]
    payload = {
            'username': user_data.username + 'new',
            'password': user_data.password.get_secret_value(),
            'email': 'new_email_' + user_data.email
            }
    response = await client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 201
    created_user = (await db_session.execute(select(User).filter_by(email=payload['email'], password_hash=sha256(payload['password'].encode('utf-8')).hexdigest()))).scalar_one_or_none()

    assert created_user is not None
    assert created_user.email == payload['email']

async def test_register_bad_email(client, db_session):
    username = str(uuid4())
    password = '12345'
    email = f'{username}@badmail'
    payload = {
        'username': username,
        'password': password,
        'email': email
        }
    response = await client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 422
    assert response.json().get('detail')[0].get('type') == 'value_error'

    user = (await db_session.execute(select(User).filter_by(username=username))).scalar_one_or_none()
    assert user is None

async def test_register_no_required_fields(client):
    payload = {
            'username': 'abc',
            'password': 'password',
            }
    response = await client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 422

async def test_register_username_already_exists(client, default_user):
    user_data = default_user[1]
    payload = {
            'username': user_data.username,
            'password': 'pass123',
            'email': 'abc_' + user_data.email
            }
    response = await client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 409
    assert response.json().get('detail') == 'A user with this username already exists.'

async def test_register_email_already_exists(client, default_user):
    user_data = default_user[1]
    payload = {
                'username': user_data.username + 'new',
                'password': 'pass123',
                'email': user_data.email
                }
    response = await client.post(API_V1_PREFIX + '/register', json=payload)

    assert response.status_code == 409
    assert response.json().get('detail') == 'A user with this email address already exists.'
    