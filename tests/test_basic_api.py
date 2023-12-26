from fastapi.testclient import TestClient

from birdweb.api import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    result = response.json()
    assert result['image_count'] >= 64  # The test file has 64 entries, a subset of what I have in my library
