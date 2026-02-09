import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_submit_valid_task():
    payload = {
        "task_title": "Implement Async Data Pipeline",
        "task_description": "Requirement: Connect to API. Objective: Pipeline data to database. Constraint: Low latency.",
        "submitted_by": "Test User"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_full_review_flow():
    # 1. Submit
    payload = {
        "task_title": "Build a Secure Async API with Pydantic and Database Schema",
        "task_description": "Objective: Implement a production-ready API. Requirement: Use async database. Constraint: Schema validation via pydantic. Tech: FastAPI, Cache, Security.",
        "submitted_by": "Review Flow User"
    }
    sub_res = client.post("/api/v1/task/submit", json=payload)
    task_id = sub_res.json()["task_id"]
    
    # 2. Review
    rev_res = client.post("/api/v1/task/review", json={"task_id": task_id})
    assert rev_res.status_code == 200
    review = rev_res.json()
    
    # Ensure contract compliance
    assert "status" in review
    assert "analysis" in review
    assert "meta" in review
    assert review["status"] in ["pass", "borderline", "fail"]
    
    # 3. Next Task
    next_res = client.post("/api/v1/task/generate-next", json=review)
    assert next_res.status_code == 200
    assert "next_task_title" in next_res.json()

def test_invalid_input_handling():
    # Too short title
    payload = {
        "task_title": "fix", 
        "task_description": "short description",
        "submitted_by": "User"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 422
    
    # Empty whitespace
    payload = {
        "task_title": "       ", 
        "task_description": "valid description long enough",
        "submitted_by": "User"
    }
    response = client.post("/api/v1/task/submit", json=payload)
    assert response.status_code == 422

def test_ad_hoc_review():
    payload = {
        "task_title": "Ad-hoc Review Title for Testing",
        "task_description": "Objective: Test ad-hoc logic. Requirement: Should work without task_id.",
        "submitted_by": "AdHoc User"
    }
    response = client.post("/api/v1/task/review", json={"payload": payload})
    assert response.status_code == 200
    assert response.json()["meta"]["mode"] == "rule"
