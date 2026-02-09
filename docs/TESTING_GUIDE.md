# Testing & Validation Guide

The system includes an automated test pipeline to ensure no regressions occur during demo usage.

## Test Categories

### 1. Unit Tests (`test_review_engine.py`)
- **Focus**: Pure logic of the `ReviewEngine`.
- **Verified Items**:
    - Determinism: Two calls with the same input yield identical results.
    - Pass/Fail/Borderline thresholds.
    - Title/Desc length logic.
    - Exact JSON schema presence.

### 2. Integration Tests (`test_api.py`)
- **Focus**: Endpoint connectivity and response models.
- **Verified Items**:
    - Full flow: `Submit -> Review -> Next Task`.
    - 422 Error handling for short/empty input.
    - Health check endpoint verification.

### 3. Security & Stress Tests (`test_security_stress.py`)
- **Focus**: Resilience against edge cases.
- **Verified Items**:
    - Max length enforcement (100 for Title, 2000 for Desc).
    - SQL injection string handling (ensures they are treated as literal text).
    - XSS string handling.
    - Malformed JSON handling.

## How to Run Tests

Ensure dependencies are installed:
```bash
pip install pytest httpx
```

Run all tests:
```bash
python -m pytest
```

## Interpreting Failures
- **AssertionError in borderline case**: The scoring logic might have shifted. Check `EVALUATION_LOGIC.md` thresholds.
- **422 Unprocessable Entity**: The input payload length or format violates `app/models/schemas.py`.
- **ModuleNotFoundError**: Ensure you are running with `python -m pytest` from the project root.
