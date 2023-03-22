from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


class TestChair:
    # ? Test storing chair information

    def test_chair_registration(self):
        item = {"chair_id": "4", "password": "123456"}
        response = client.post("/chair/signup/", json=item)
        assert response.status_code == 201
        assert response.json() == {"message": "Chair register successfully"}

    def test_chair_registration_wrong(self):
        item = {"chair_id": "112321", "password": "123456"}
        response = client.post("/chair/signup/", json=item)
        assert response.status_code == 400
        assert response.json() == {"detail": "This Chair ID is already exist"}

    # ? Test login to chair

    def test_chair_login(self):
        item = {"chair_id": "50", "password": "mypassword"}
        response = client.post("/chair/login/", json=item)
        assert response.status_code == 200
        assert response.json() == {"message": "Chair login successfully"}

    def test_chair_login_wrong(self):
        item = {"chair_id": "7", "password": "mypassword12"}
        response = client.post("/chair/login/", json=item)
        assert response.status_code == 404
        assert response.json() == {"detail": "Chair ID or Password Invalid"}

    # ? Test storing senors' data

    def test_post_chair_data(self):
        item = {
            "temperature": "36.5",
            "oximeter": "125.4",
            "pulse_rate": "122.5",
            "sugar_level": "70.45",
            "chair_id": "50",
        }
        response = client.post("/chair/data/", json=item)
        assert response.status_code == 201
        assert response.json() == {"message": "Data has been stored successfully"}

    def test_post_chair_data_wrong(self):
        item = {
            "temperature": "36.5",
            "oximeter": "125.4",
            "pulse_rate": "122.5",
            "sugar_level": "70.45",
            "chair_id": "999",
        }
        response = client.post("/chair/data/", json=item)
        assert response.status_code == 404
        assert response.json() == {"detail": "No Chair stored with this ID"}

    # ? Test retriving sensors' data

    def test_get_chair_data(self):
        response = client.get("/chair/data/50")
        assert response.status_code == 200
        assert response.json() == {
            "temperature": 36.5,
            "oximeter": 125.4,
            "pulse_rate": 122.5,
            "sugar_level": 70.45,
        }

    def test_get_chair_data_wrong(self):
        response = client.get("/chair/data/88888")
        assert response.status_code == 404
        assert response.json() == {"detail": "Data not found"}
