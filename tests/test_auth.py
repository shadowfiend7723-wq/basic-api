from fastapi.testclient import TestClient

from app import database
from app.main import app
from app.register import password_hasher


class FakeUsers:
    def __init__(self) -> None:
        self.documents: dict[str, dict[str, str]] = {}

    def find_one(self, query: dict[str, str]) -> dict[str, str] | None:
        return self.documents.get(query["username"])

    def insert_one(self, document: dict[str, str]) -> None:
        self.documents[document["username"]] = document


def test_register_stores_a_hashed_password(monkeypatch) -> None:
    fake_users = FakeUsers()
    monkeypatch.setattr(database, "users", fake_users)
    client = TestClient(app)

    response = client.post(
        "/register",
        data={"username": "nova", "password": "correct-horse"},
    )

    assert response.status_code == 201
    assert response.json() == {"message": "Welcome, nova"}
    stored_user = fake_users.documents["nova"]
    assert stored_user["password"] != "correct-horse"
    assert password_hasher.verify(stored_user["password"], "correct-horse")


def test_register_rejects_duplicate_username(monkeypatch) -> None:
    fake_users = FakeUsers()
    fake_users.documents["nova"] = {"username": "nova", "password": "hashed"}
    monkeypatch.setattr(database, "users", fake_users)

    response = TestClient(app).post(
        "/register",
        data={"username": "nova", "password": "correct-horse"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already taken"


def test_login_accepts_correct_password_and_rejects_invalid_credentials(
    monkeypatch,
) -> None:
    fake_users = FakeUsers()
    fake_users.documents["nova"] = {
        "username": "nova",
        "password": password_hasher.hash("correct-horse"),
    }
    monkeypatch.setattr(database, "users", fake_users)
    client = TestClient(app)

    success = client.post(
        "/login",
        data={"username": "nova", "password": "correct-horse"},
    )
    wrong_password = client.post(
        "/login",
        data={"username": "nova", "password": "wrong-password"},
    )
    unknown_user = client.post(
        "/login",
        data={"username": "missing", "password": "correct-horse"},
    )

    assert success.status_code == 200
    assert success.json() == {"message": "Welcome, nova"}
    assert wrong_password.status_code == 401
    assert unknown_user.status_code == 401
