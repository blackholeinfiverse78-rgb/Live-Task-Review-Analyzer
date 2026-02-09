# Evaluation Logic & Scoring Engine

The `ReviewEngine` is the core intelligence of the system. It uses a deterministic, rule-based approach to score engineering tasks.

## Scoring Dimensions (Total 100 pts)

### 1. Title Context (15 Points)
- **Goal**: Ensure the title is descriptive enough to stand alone.
- **Logic**:
    - `> 40 chars`: 15 pts (Professional depth)
    - `> 20 chars`: 10 pts (Adequate)
    - `< 20 chars`: 5 pts (Flags "Brief title reduces context")

### 2. Description Substance (30 Points)
- **Goal**: Ensure technical depth in the task body.
- **Logic**:
    - `> 500 chars`: 30 pts (Comprehensive)
    - `> 200 chars`: 20 pts (Detailed)
    - `> 50 chars`: 10 pts (Basic)
    - `< 50 chars`: 0 pts (Flags "Minimal description substance")

### 3. Logical Markers (30 Points)
- **Goal**: Identify standard engineering discipline signals.
- **Logic**: Scans for the literal presence (case-insensitive) of:
    - `requirement`: 10 pts
    - `objective`: 10 pts
    - `constraint`: 10 pts
- Missing markers trigger specific `failure_reasons` and `improvement_hints`.

### 4. Technical Specificity (25 Points)
- **Goal**: Ensure the task mentions Implementation-level details.
- **Keywords**: `api`, `database`, `schema`, `validation`, `security`, `async`, `cache`, `frontend`, `readme`, `documentation`, `test`, `coverage`.
- **Logic**: `min(25, count(keywords_found) * 5)`.
- Finding fewer than 2 keywords triggers "Low technical specificity".

## Result Normalization

### Readiness Percentage
- Calculated as `score * 0.85` for scores under 90.
- High scores (90+) are treated as fully ready (`readiness_percent = score`).

### Status Mapping
- **PASS**: Score >= 85
- **BORDERLINE**: Score 60 - 84
- **FAIL**: Score < 60

### Analysis Metrics
Calculated as percentages of their sub-components:
- **Technical Quality**: (tech\_keywords\_score / 25) * 100
- **Clarity**: ((title\_score + desc\_score) / 45) * 100
- **Discipline Signals**: (marker\_score / 30) * 100
