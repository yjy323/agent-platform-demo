from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root() -> None:
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World! Welcome to Test API"}


def test_health_check() -> None:
    """헬스 체크 엔드포인트 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
