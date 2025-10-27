import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_index_redirects(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/calculator" in response.headers["Location"]


def test_addition(client):
    response = client.post(
        "/calculator",
        data={"operand_a": "5", "operand_b": "7", "operator": "+"},
        follow_redirects=True,
    )
    assert b"Result" in response.data
    assert b"12" in response.data


def test_division_by_zero(client):
    response = client.post(
        "/calculator",
        data={"operand_a": "5", "operand_b": "0", "operator": "/"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Division by zero" in response.data
