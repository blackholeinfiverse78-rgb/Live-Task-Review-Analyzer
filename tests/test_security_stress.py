import pytest
from fastapi.testclient import TestClient
from app.main import app
import string
import random

client = TestClient(app)

def test_max_length_enforcement():
    # task_title max_length=100
    long_title = "a" * 101
    payload = {
        "task_title": long_title,
        "task_description": "Valid description long enough",
        "submitted_by": "User"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 422
    assert "task_title" in str(response.json())

    # task_description max_length=2000
    long_desc = "a" * 2001
    payload = {
        "task_title": "Valid Title",
        "task_description": long_desc,
        "submitted_by": "User"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 422
    assert "task_description" in str(response.json())

def test_sql_injection_simulation():
    # Since we use in-memory dict, it's safe, but we check if it breaks the system
    payload = {
        "task_title": "SELECT * FROM users; --",
        "task_description": "DROP TABLE tasks; CASCADE; ' OR '1'='1",
        "submitted_by": "Hacker"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 200 # Should be treated as normal string
    task_id = response.json()["task_id"]
    
    review_res = client.post("/api/v1/task/review", json={"task_id": task_id})
    assert review_res.status_code == 200

def test_xss_simulation():
    payload = {
        "task_title": "<script>alert('xss')</script>",
        "task_description": "Check XSS: <img src=x onerror=alert(1)>",
        "submitted_by": "Hacker"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 200 # Treated as string
    
    task_id = response.json()["task_id"]
    review_res = client.post("/api/v1/task/review", json={"task_id": task_id})
    assert review_res.status_code == 200
    # The frontend is responsible for escaping, but backend should handle the storage.

def test_unauthorized_access():
    # Test accessing non-existent task
    response = client.post("/api/v1/task/review", json={"task_id": "non-existent-uuid"})
    assert response.status_code == 404

def test_malformed_json():
    response = client.post("/api/v1/task/submit", content="invalid json", headers={"Content-Type": "application/json"})
    assert response.status_code == 422
