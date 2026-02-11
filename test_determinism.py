
import requests
import json
import hashlib

BASE_URL = "http://localhost:8000/api/v1/task"

def get_review(payload):
    res_submit = requests.post(f"{BASE_URL}/submit", json=payload)
    task_id = res_submit.json().get("task_id")
    res_review = requests.post(f"{BASE_URL}/review", json={"task_id": task_id})
    return res_review.json()

valid_full = {
    "task_title": "Build a Secure Async API Gateway for User Authentication and Management",
    "task_description": "The objective is to implement a robust API gateway. Requirements include schema validation using Pydantic, security constraints for JWT, and async database connections. This task ensures production readiness by adding caching and frontend integration layers. Final success criteria: 100% test coverage and full documentation.",
    "submitted_by": "Test User"
}

print("--- Testing Determinism (5 iterations) ---")
results = []
for i in range(5):
    review = get_review(valid_full)
    # Remove metadata that changes (evaluation_time_ms)
    review['meta'].pop('evaluation_time_ms', None)
    results.append(json.dumps(review, sort_keys=True))

first_hash = hashlib.sha256(results[0].encode()).hexdigest()
is_deterministic = True
for i, res in enumerate(results):
    current_hash = hashlib.sha256(res.encode()).hexdigest()
    print(f"Iteration {i+1} Hash: {current_hash}")
    if current_hash != first_hash:
        is_deterministic = False

if is_deterministic:
    print("SUCCESS: Output is deterministic (excluding execution time).")
else:
    print("FAILURE: Output varies between runs!")
