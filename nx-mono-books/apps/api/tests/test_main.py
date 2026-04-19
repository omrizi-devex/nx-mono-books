from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_greet_endpoint():
    response = client.get("/hello/Alice")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Alice!"}