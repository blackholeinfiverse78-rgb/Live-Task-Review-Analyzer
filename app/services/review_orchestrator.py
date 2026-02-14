from ..core.interfaces.review_engine_interface import ReviewEngineInterface
from ..core.interfaces.next_task_interface import NextTaskGeneratorInterface
from ..models.schemas import Task, ReviewOutput, Analysis, Meta
from ..models.orchestration import OrchestrationResult, V2NextTask
from ..models.task_templates import SYSTEM_FALLBACK_TASK
import logging

logger = logging.getLogger("orchestrator")

class ReviewOrchestrator:
    def __init__(
        self,
        review_engine: ReviewEngineInterface,
        next_task_generator: NextTaskGeneratorInterface,
    ):
        self._review_engine = review_engine
        self._next_task_generator = next_task_generator

    @staticmethod
    def classify_readiness(score: int) -> str:
        """
        Deterministic readiness classification based on score bands.
        85+   -> PASS
        60-84 -> BORDERLINE
        <60   -> FAIL
        """
        # Edge case handling for out-of-bounds scores
        if score < 0:
            score = 0
        elif score > 100:
            score = 100

        if score >= 85:
            return "PASS"
        elif score >= 60:
            return "BORDERLINE"
        else:
            return "FAIL"

    def process_submission(self, task: Task) -> OrchestrationResult:
        """
        Orchestrates the review process with high observability and robustness.
        """
        logger.info(f"Starting orchestration for task: {task.task_id}")
        
        try:
            # 1. Call ReviewEngine
            review_result_dict = self._review_engine.evaluate(task.model_dump())
            review_output = ReviewOutput(**review_result_dict)
            logger.info(f"ReviewEngine completed. Score: {review_output.score}")
        except Exception as e:
            logger.error(f"ReviewEngine failed: {str(e)} - Generating safety result")
            # Deterministic failure fallback for Review Logic
            review_output = ReviewOutput(
                score=0,
                readiness_percent=0,
                status="fail",
                failure_reasons=["System: Review process encountered a critical error."],
                analysis=Analysis(technical_quality=0, clarity=0, discipline_signals=0),
                meta=Meta(evaluation_time_ms=0, mode="rule")
            )

        # 2. Interpret readiness
        classification = self.classify_readiness(review_output.score)
        logger.info(f"Decision Path: Score {review_output.score} mapped to band: {classification}")

        # 3. Pass classification to NextTaskGenerator with robustness
        try:
            next_task = self._next_task_generator.generate_next_task(review_output, classification)
            logger.info(f"NextTaskGenerator success: {next_task.title}")
        except Exception as e:
            logger.warning(f"NextTaskGenerator failed: {str(e)} - Triggering SYSTEM_FALLBACK")
            next_task = V2NextTask(
                title=SYSTEM_FALLBACK_TASK.title,
                objective=SYSTEM_FALLBACK_TASK.objective,
                focus_area=SYSTEM_FALLBACK_TASK.focus_area,
                difficulty=SYSTEM_FALLBACK_TASK.difficulty
            )

        # 4. Attach next_task to review_output for backward compatible extension
        review_output.next_task = next_task

        # 5. Return structured response
        return OrchestrationResult(
            review=review_output,
            readiness_classification=classification,
            next_task=next_task
        )
