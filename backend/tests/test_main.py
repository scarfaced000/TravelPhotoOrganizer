import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["version"] == "1.0.0"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "timestamp" in data

def test_list_photos():
    """Test list photos endpoint"""
    response = client.get("/api/v1/photos")
    assert response.status_code == 200
    photos = response.json()
    assert isinstance(photos, list)
    assert len(photos) == 5

def test_list_albums():
    """Test list albums endpoint"""
    response = client.get("/api/v1/albums")
    assert response.status_code == 200
    albums = response.json()
    assert isinstance(albums, list)
    assert len(albums) == 2

def test_get_album():
    """Test get album endpoint"""
    response = client.get("/api/v1/albums/test_id")
    assert response.status_code == 200
    album = response.json()
    assert album["id"] == "test_id"
    assert "name" in album
