import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
    ('k0t@pes.com', '123456', 200),
    ('k0t@pes.com', '123456', 409),
    ('k0t1@pes.com', '123456', 200),
    ('abcde', '123456', 422),
    ('abcde@abc', '123456', 422),
])
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    # /register
    resp_register = await ac.post(
        '/auth/register',
        json={
            'email': email,
            'password': password,
        }
    )
    assert resp_register.status_code == status_code
    if status_code != 200:
        return

    # /login
    resp_login = await ac.post(
            '/auth/login',
        json={
            'email': email,
            'password': password,
        }
    )
    assert resp_login.status_code == 200
    assert ac.cookies['access_token']
    assert 'access_token' in resp_login.json()

    # /me
    resp_me = await ac.get('/auth/me')
    assert resp_me.status_code == 200
    user = resp_me.json()
    assert user['email'] == email
    assert 'id' in user
    assert 'password' not in user
    assert 'hashed_password' not in user

    # /logout
    resp_logout = await ac.post('/auth/logout')
    assert resp_logout.status_code == 200
    assert 'access_token' not in ac.cookies


async def test_register_user(ac: AsyncClient):
    response = await ac.post(
        '/auth/register',
        json={
            'email': 'test@example.com',
            'password': 'password123'
        }
    )
    assert response.status_code == 200

async def test_login_user(ac: AsyncClient):
    response = await ac.post(
        '/auth/login',
        json={
            'email': 'test@example.com',
            'password': 'password123'
        }
    )
    assert response.status_code == 200
    assert response.json()['access_token']

async def test_logout_only_once(ac: AsyncClient):
    response1 = await ac.post('/auth/logout')
    assert response1.status_code == 200

    response2 = await ac.post('/auth/logout')
    assert response2.status_code == 400

async def test_cannot_logout_without_token(ac: AsyncClient):
    response = await ac.post('/auth/logout')
    assert response.status_code == 400

async def test_cannot_register_with_empty_password(ac: AsyncClient):
    response = await ac.post(
        '/auth/register',
        json={
            'email': 'test2@example.com',
            'password': '',
        },
    )
    assert response.status_code == 422

async def test_cannot_login_with_empty_password(ac: AsyncClient):
    response = await ac.post(
        '/auth/login',
        json={
            'email': 'test@example.com',
            'password': '',
        },
    )
    assert response.status_code == 422
