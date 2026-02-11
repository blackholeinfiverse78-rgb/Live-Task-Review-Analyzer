# 🛡️ Live Task Review Agent (Production Demo)

Deterministic engineering task assessment system designed for high-reliability technical audits. This system evaluates task definitions against rigorous engineering standards using a modular, rule-based engine.

## 🏁 Demo Deployment
1. **Start Backend**: `python -m app.main`
   - URL: `http://localhost:8000`
   - Health: `http://localhost:8000/health`
2. **Start Frontend**: `python -m streamlit run frontend/streamlit_app.py`
   - URL: `http://localhost:8501`

## 🎯 System Capabilities
- **Deterministic Scoring**: Identical input always yields identical results.
- **Contract Enforcement**: 100% adherence to JSON output schemas (even on failures).
- **Rule-Based Intelligence**: Evaluates Title Depth, Description Substance, Logical Markers, and Technical Specificity.
- **Zero-Dependency Storage**: Uses high-speed in-memory persistence for demo environments.

## 📝 Mandatory JSON Contract
All evaluations return this exact structure:
```json
{
  "score": 0-100,
  "readiness_percent": 0-100,
  "status": "pass" | "borderline" | "fail",
  "failure_reasons": ["strings"],
  "improvement_hints": ["strings"],
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

## 🧪 Demo Scenarios
| Scenario | Input Type | Expected Status | Description |
| :--- | :--- | :--- | :--- |
| **Pass** | Full context | `PASS` | High-quality task with all markers and tech keywords. |
| **Borderline** | Partial context | `BORDERLINE` | Lacks technical specificity but has basic structure. |
| **Fail** | Minimal | `FAIL` | Too short, lacks any engineering discipline signals. |
| **Safety** | Invalid/Empty | `FAIL` | Triggers standardized failure contract with validation errors. |

## 🛠️ Performance & Security
- **Latency**: < 5ms processing time per evaluation.
- **Safety**: Strict Pydantic validation for all inputs (Title: 5-100, Desc: 10-2000 characters).
- **Audit**: Bandit verified - 0 security vulnerabilities.
