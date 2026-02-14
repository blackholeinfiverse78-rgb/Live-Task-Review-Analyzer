import pytest
import json
import io
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_repeated_call_determinism():
    """
    Validation Test: Ensuring that multiple identical requests produce
    the exact same score, status, and analysis breakdown.
    """
    
    # Setup consistent mock for GitHub API calls
    mock_metrics = {
        "full_name": "test/repo",
        "default_branch": "main",
        "commit_count": 50,
        "has_readme": True,
        "has_tests": True,
        "file_count": 100,
        "stargazers_count": 10,
        "forks_count": 5,
        "private": False,
        "updated_at": "2026-02-14T12:00:00Z"
    }

    # Consistent PDF content
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n..." # Mock binary
    
    with patch("app.services.repo_analyzer.RepoAnalyzer.analyze_repo", return_value=mock_metrics), \
         patch("app.services.pdf_processor.PDFProcessor.extract_text", return_value="Objective: High quality project document.\nStructured Heading\n" + "Word " * 100):
        
        results = []
        for i in range(5):
            # Create a new file-like object for each request to simulate fresh upload
            pdf_file = io.BytesIO(pdf_content)
            
            response = client.post(
                "/api/v1/task/review",
                data={
                    "github_url": "https://github.com/test/repo",
                    "description": "Deterministic audit request for repeated calling validation."
                },
                files={"pdf_file": ("test.pdf", pdf_file, "application/pdf")}
            )
            
            assert response.status_code == 200
            results.append(response.json())

        # Validate that all results are identical
        first_res = results[0]
        for i, res in enumerate(results[1:], start=1):
            # We compare the entire dictionary except for any meta/uuid fields if they existed
            # (But our ReviewOutput is designed to be deterministic)
            assert res["score"] == first_res["score"], f"Iteration {i}: Score mismatch"
            assert res["status"] == first_res["status"], f"Iteration {i}: Status mismatch"
            assert res["analysis"] == first_res["analysis"], f"Iteration {i}: Analysis mismatch"
            assert res["meta"]["evaluation_time_ms"] == first_res["meta"]["evaluation_time_ms"], f"Iteration {i}: Latency mismatch"
            
        print(f"SUCCESS: 5/5 iterations produced identical output. Score: {first_res['score']}")

if __name__ == "__main__":
    pytest.main([__file__])
