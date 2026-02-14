from pydantic import BaseModel
from .schemas import ReviewOutput, NextTask, V2NextTask

class OrchestrationResult(BaseModel):
    review: ReviewOutput
    readiness_classification: str
    next_task: V2NextTask
