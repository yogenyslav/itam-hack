from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.app import create_app

app = create_app()


client = TestClient(app)


def test_user_signup():
    response = client.post(
        "/auth/signup",
        json={
            "email": "test100@test.com",
            "password": "test123456",
            "first_name": "Денис",
            "last_name": "Трипольский",
            "internal_role": "admin",
        },
    )
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # try create user with same email
    response = client.post(
        "/auth/signup",
        json={
            "email": "test100@test.com",
            "password": "test123456",
            "first_name": "Денис",
            "last_name": "Трипольский",
            "internal_role": "admin",
        },
    )
    assert response.status_code == 400
    assert "detail" in response.json()


def test_user_login():
    response = client.post(
        "/auth/login",
        json={"email": "test100@test.com", "password": "test123456"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    # test invalid password

    response = client.post(
        "/auth/login",
        json={"email": "test100@test.com", "password": "test123456"},
    )

    assert response.status_code == 401


def test_create_multiple_users():
    response = client.post(
        "/auth/signup",
        json={
            "email": "
# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}
