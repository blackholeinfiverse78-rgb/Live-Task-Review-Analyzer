"""
Task Review AI - Modular Engine v2.1
Updated on: 2026-02-05
Logic: Modular Deterministic Rule Evaluators
"""
from ..models.schemas import Task, ReviewOutput, Analysis, Meta
import logging
import time

logger = logging.getLogger("task_review_system")

class ReviewEngine:
    @staticmethod
    def _evaluate_title(title: str, failure_reasons: list, hints: list) -> int:
        t_len = len(title)
        if t_len > 40:
            return 15
        if t_len > 20:
            return 10
        failure_reasons.append("Brief title reduces context.")
        hints.append("Expand title to 40+ characters.")
        return 5

    @staticmethod
    def _evaluate_description(description: str, failure_reasons: list, hints: list) -> int:
        d_len = len(description)
        if d_len > 500:
            return 30
        if d_len > 200:
            return 20
        if d_len > 50:
            return 10
        failure_reasons.append("Minimal description substance.")
        hints.append("Provide detailed technical context.")
        return 0

    @staticmethod
    def _evaluate_markers(description: str, failure_reasons: list, hints: list) -> int:
        score = 0
        description_lower = description.lower()
        for marker in ["requirement", "objective", "constraint"]:
            if marker in description_lower:
                score += 10
            else:
                failure_reasons.append(f"Missing logical marker: '{marker}'")
                hints.append(f"Define task {marker}s.")
        return score

    @staticmethod
    def _evaluate_technical_keywords(description: str, failure_reasons: list, hints: list) -> int:
        tech = ["api", "database", "schema", "validation", "security", "async", "cache", "frontend", "readme", "documentation", "test", "coverage"]
        description_lower = description.lower()
        found = [k for k in tech if k in description_lower]
        score = min(25, len(found) * 5)
        
        if len(found) < 2:
            failure_reasons.append("Low technical specificity.")
            hints.append("Include technical implementation details (e.g., API, Database, Schema).")
        return score

    @classmethod
    def review_task(cls, task: Task) -> ReviewOutput:
        """
        Pure deterministic review processor. Same Input -> Same Output.
        Now strictly enforces the mandatory JSON contract.
        """
        start_time = time.time()
        
        failure_reasons = []
        hints = []
        
        # Component scores
        title_score = cls._evaluate_title(task.task_title, failure_reasons, hints)
        desc_score = cls._evaluate_description(task.task_description, failure_reasons, hints)
        marker_score = cls._evaluate_markers(task.task_description, failure_reasons, hints)
        tech_score = cls._evaluate_technical_keywords(task.task_description, failure_reasons, hints)
        
        final_score = min(100, title_score + desc_score + marker_score + tech_score)
        readiness = int(final_score * 0.85) if final_score < 90 else final_score
        
        # Status Mapping
        if final_score >= 85:
            status = "pass"
        elif final_score >= 60:
            status = "borderline"
        else:
            status = "fail"

        # Analysis Normalization
        analysis = Analysis(
            technical_quality=int((tech_score / 25) * 100),
            clarity=int(((title_score + desc_score) / 45) * 100),
            discipline_signals=int((marker_score / 30) * 100)
        )
        
        # Meta calculation
        eval_duration = int((time.time() - start_time) * 1000)
        meta = Meta(
            evaluation_time_ms=max(1, eval_duration),
            mode="rule"
        )

        return ReviewOutput(
            score=final_score,
            readiness_percent=readiness,
            status=status,
            failure_reasons=failure_reasons,
            improvement_hints=hints,
            analysis=analysis,
            meta=meta
        )
