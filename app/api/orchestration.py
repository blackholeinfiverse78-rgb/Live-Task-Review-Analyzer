from fastapi import APIRouter, Depends
from ..models.schemas import Task, ReviewOutput, NextTask
from ..models.orchestration import OrchestrationResult
from ..services.review_orchestrator import ReviewOrchestrator
from ..core.dependencies import get_review_orchestrator

router = APIRouter()

@router.post("/process", response_model=OrchestrationResult)
async def process_task_submission(
    task: Task,
    orchestrator: ReviewOrchestrator = Depends(get_review_orchestrator)
):
    """
    Main entry point for the autonomous review process.
    """
    return orchestrator.process_submission(task)
