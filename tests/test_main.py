import pytest
from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello from GitHub Actions Demo!' in response.data


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_add(client):
    response = client.get('/add?a=5&b=3')
    assert response.status_code == 200
    assert response.get_json()['result'] == 8


def test_add_negative(client):
    response = client.get('/add?a=-5&b=3')
    assert response.get_json()['result'] == -2


def test_divide(client):
    response = client.get('/divide?a=10&b=2')
    assert response.get_json()['result'] == 5.0


def test_divide_by_zero(client):
    response = client.get('/divide?a=10&b=0')
    assert response.status_code == 400
    assert 'error' in response.get_json()
