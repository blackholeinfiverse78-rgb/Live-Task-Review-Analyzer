# API Contracts & JSON Specifications

This document defines the exact payloads and responses for the Live Task Review Agent.

## 1. Task Submission
- **POST** `/api/v1/task/submit`

### Request Body
```json
{
  "task_title": "string (5-100 characters)",
  "task_description": "string (10-2000 characters)",
  "submitted_by": "string (2-50 characters)"
}
```

### Response (200 OK)
```json
{
  "task_id": "uuid-string",
  "task_title": "...",
  "task_description": "...",
  "submitted_by": "...",
  "timestamp": "iso-datetime"
}
```

## 2. Task Review
- **POST** `/api/v1/task/review`

### Request Body (By ID)
```json
{
  "task_id": "uuid-string"
}
```

### Request Body (Ad-hoc)
```json
{
  "payload": {
    "task_title": "...",
    "task_description": "...",
    "submitted_by": "..."
  }
}
```

### Response (200 OK) - Mandatory Output Contract
```json
{
  "score": 0-100,
  "readiness_percent": 0-100,
  "status": "pass" | "borderline" | "fail",
  "failure_reasons": ["string"],
  "improvement_hints": ["string"],
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

## 3. Next Task Generation
- **POST** `/api/v1/task/generate-next`

### Request Body
Pass the exact JSON response from the Review endpoint.

### Response (200 OK)
```json
{
  "next_task_title": "string",
  "next_task_description": "string",
  "difficulty_level": "easy" | "medium" | "hard",
  "rationale": "string"
}
```

## Error Codes
- **404 Not Found**: Task ID does not exist.
- **422 Unprocessable Entity**: Validation failed (e.g., text too short, missing fields).
- **500 Internal Error**: Fatal processing error.
