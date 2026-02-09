# Live Task Review Agent (Gurukul Adaptive Assessment)

Deterministic engineering task analysis system designed to evaluate task definitions for technical readiness. This system strictly enforces a modular evaluation logic and a predefined JSON output contract.

## 🚀 Quick Start
1. **Launch Backend**: `python -m app.main` (Available at http://localhost:8000)
2. **Launch Frontend**: `python -m streamlit run frontend/streamlit_app.py` (Available at http://localhost:8501)
3. **Run Validation Tests**: `python -m pytest`

## 🛠️ API Reference

### 1. Submit Task for Persistence
- **Endpoint**: `POST /api/v1/task/submit`
- **Payload**:
  ```json
  {
    "task_title": "Build a Secure Async API",
    "task_description": "Requirement: Connect to DB. Objective: Production ready API.",
    "submitted_by": "Developer Name"
  }
  ```
- **Response**: Returns a `Task` object with a generated `task_id`.

### 2. Review Existing Task
- **Endpoint**: `POST /api/v1/task/review`
- **Payload**:
  ```json
  {
    "task_id": "uuid-of-task"
  }
  ```
- **Alternate (Ad-hoc)**:
  ```json
  {
    "payload": {
      "task_title": "...", 
      "task_description": "...", 
      "submitted_by": "..."
    }
  }
  ```

### 3. Transition Recommendation
- **Endpoint**: `POST /api/v1/task/generate-next`
- **Payload**: Accepts the exact `ReviewOutput` produced by the review endpoint.

---

## 📊 Evaluation Logic & Scoring
The system uses a **Deterministic Rule Engine** (`ReviewEngine.py`) to calculate scores:
- **Title Depth (15 pts)**: Scoring increases with title length (thresholds: 20, 40 chars).
- **Description Substance (30 pts)**: Scoring based on text length (thresholds: 50, 200, 500 chars).
- **Logical Markers (30 pts)**: Identifies presence of `requirement`, `objective`, and `constraint`.
- **Technical Specificity (25 pts)**: Scans for keywords like `api`, `database`, `schema`, `validation`, `security`, `async`, `cache`, `frontend`, `documentation`, `test`.

### Verbatim Output Specification (Implemented)
All evaluation results strictly adhere to this schema:
```json
{
  "score": 0-100,
  "readiness_percent": 0-100,
  "status": "pass" | "borderline" | "fail",
  "failure_reasons": ["List of detected gaps"],
  "improvement_hints": ["Actionable optimization steps"],
  "analysis": {
    "technical_quality": 0-100,
    "clarity": 0-100,
    "discipline_signals": 0-100
  },
  "meta": {
    "evaluation_time_ms": number,
    "mode": "rule"
  }
}
```

---

## 🧪 Automated Test Suite
The repository includes a comprehensive `pytest` suite located in `/tests`:
- `test_review_engine.py`: Unit tests for scoring logic, pass/fail cases, and determinism.
- `test_api.py`: Full end-to-end integration tests for all REST endpoints.
- `test_security_stress.py`: Audits for SQLi/XSS simulation, length enforcement, and malformed inputs.

Run tests using:
```bash
python -m pytest
```

## 🛡️ Security Audit
- **CORS Hardening**: Configured middleware for safe cross-origin demo interactions.
- **Input Sanitization**: Pydantic-enforced character constraints and length limits.
- **Bandit Verified**: Security scan confirmed 0 High/Medium issues.
