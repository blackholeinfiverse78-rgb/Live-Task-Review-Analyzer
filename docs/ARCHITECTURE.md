# System Architecture

The Live Task Review Agent is built with a focus on **determinism, reliability, and clear technical feedback**. It follows a modular micro-service style architecture even within its monolithic structure.

## Component Overview

### 1. Frontend (Streamlit)
- **Role**: User Interface for demo and manual input.
- **Tech**: Streamlit.
- **Key Functions**:
    - Input capturing (Title, Description).
    - Scenario selection (Good, Partial, Poor).
    - Visual representation of score, readiness, and progress bars.
    - Displaying "Next Task" recommendations.

### 2. Backend (FastAPI)
- **Role**: RESTful API and core logic execution.
- **Tech**: FastAPI, Pydantic, uvicorn.
- **Structure**:
    - `api/`: Route definitions for submission, review, and next task generation.
    - `models/`: Pydantic schemas for request/response validation and in-memory storage.
    - `services/`: Core engines (`ReviewEngine`, `NextTaskEngine`).

### 3. Evaluation Engine (Deterministic Rule-Based)
- **Role**: Analyze task text and produce scores.
- **Methodology**: Avoids LLM non-determinism. Uses regex, string length analysis, and keyword matching.
- **Normalization**: Translates raw points into the mandatory JSON schema.

## Data Flow
1. **Submission**: User submits a task via Frontend -> Backend `/submit`.
2. **Storage**: Backend generates a `task_id` and stores it in-memory.
3. **Review**: Frontend calls `/review` with `task_id`.
4. **Analysis**: `ReviewEngine` evaluates the stored task string.
5. **JSON Contract**: engine returns a strictly structured response.
6. **Recommendation**: Frontend calls `/generate-next` to get the transition task.

## In-Memory Storage
For the demo phase, storage is managed via a simple Python dictionary (`app/models/storage.py`). This ensures high speed and zero database dependency for on-prem demos.
