from fastapi import Depends
from ..core.interfaces.review_engine_interface import ReviewEngineInterface
from ..core.interfaces.next_task_interface import NextTaskGeneratorInterface
from ..services.review_engine import ReviewEngine
from ..services.sequential_task_generator import SequentialTaskGenerator
from ..services.review_orchestrator import ReviewOrchestrator

def get_review_engine() -> ReviewEngineInterface:
    """Dependency Provider for Review Engine"""
    return ReviewEngine()

def get_next_task_generator() -> NextTaskGeneratorInterface:
    """Dependency Provider for Next Task Generator"""
    return SequentialTaskGenerator()

def get_review_orchestrator(
    review_engine: ReviewEngineInterface = Depends(get_review_engine),
    next_task_generator: NextTaskGeneratorInterface = Depends(get_next_task_generator)
) -> ReviewOrchestrator:
    """Dependency Provider for Review Orchestrator"""
    return ReviewOrchestrator(review_engine, next_task_generator)
