from app.main import API_V1_PREFIX


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

def test_login_required_fields_missing(client, default_user):
    payload = {
            'email': default_user.email
        }
    
    response = client.post(API_V1_PREFIX + '/login', json=payload)
    assert response.status_code == 422

    payload = {
            'password': default_user.password.get_secret_value()
        }
    response = client.post(API_V1_PREFIX + '/login', json=payload)
    assert response.status_code == 422

    response = client.post(API_V1_PREFIX + '/login', json={})
    assert response.status_code == 422

def test_login_empty_body(client, default_user):
    response = client.post(API_V1_PREFIX + '/login')
    assert response.status_code == 422
