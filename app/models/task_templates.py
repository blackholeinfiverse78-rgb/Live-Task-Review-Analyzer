from pydantic import BaseModel
from typing import Dict

class TaskTemplate(BaseModel):
    title: str
    objective: str
    focus_area: str
    difficulty: str
    rationale: str

class NextTaskRules(BaseModel):
    pass_task: TaskTemplate
    borderline_task: TaskTemplate
    fail_task: TaskTemplate

# Deterministic Fallback for System Robustness
SYSTEM_FALLBACK_TASK = TaskTemplate(
    title="General Task Review & Cleanup",
    objective="System Fallback: Review the current state of the project and perform general cleanup.",
    focus_area="Architecture, Cleanup, Documentation",
    difficulty="medium",
    rationale="NextTaskGenerator encountered an issue. Reverted to a safe default task to ensure continuity."
)
