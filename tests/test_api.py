import os

os.environ["DATABASE_URL"] = "sqlite:///./test_taskflow.db"
os.environ["SECRET_KEY"] = "test-secret-key"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_taskflow.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    return TestClient(app)


def register_and_login(client, username="sagar", email="sagar@example.com"):
    register_response = client.post(
        "/auth/register",
        json={"username": username, "email": email, "password": "strongpass123"},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": username, "password": "strongpass123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_user_can_register_login_and_manage_tasks(client):
    headers = register_and_login(client)

    create_response = client.post(
        "/tasks/",
        headers=headers,
        json={"title": "Finish API polish", "description": "Add tests and deployment files"},
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["title"] == "Finish API polish"
    assert task["completed"] is False

    list_response = client.get("/tasks/", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/tasks/{task['id']}",
        headers=headers,
        json={"completed": True},
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    delete_response = client.delete(f"/tasks/{task['id']}", headers=headers)
    assert delete_response.status_code == 204


def test_users_cannot_read_each_others_tasks(client):
    first_user_headers = register_and_login(client, "first_user", "first@example.com")
    task_response = client.post(
        "/tasks/",
        headers=first_user_headers,
        json={"title": "Private task"},
    )
    task_id = task_response.json()["id"]

    second_user_headers = register_and_login(client, "second_user", "second@example.com")
    response = client.get(f"/tasks/{task_id}", headers=second_user_headers)

    assert response.status_code == 404


def test_protected_routes_require_authentication(client):
    response = client.get("/tasks/")

    assert response.status_code == 401
