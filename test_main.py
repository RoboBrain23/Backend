from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_chair_registeration():
    item = {"chair_id": "112321", "password": "123456"}
    response = client.post("/chair/signup/", json=item)
    assert response.status_code == 201
    assert response.json() == {"message": "Chair register successfully"}
