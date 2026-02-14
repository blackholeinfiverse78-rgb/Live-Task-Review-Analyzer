from ..core.interfaces.next_task_interface import NextTaskGeneratorInterface
from ..models.schemas import ReviewOutput
from ..models.orchestration import V2NextTask
from ..models.task_templates import TaskTemplate, NextTaskRules

class SequentialTaskGenerator(NextTaskGeneratorInterface):
    """
    Deterministic rule-based task generator.
    Implements:
    PASS -> Stretch Task
    BORDERLINE -> Reinforcement Task
    FAIL -> Correction Task
    """
    
    # Predefined strict mapping - No AI generation
    RULES = NextTaskRules(
        pass_task=TaskTemplate(
            title="System Scalability & Performance Optimization",
            objective="Stretch Task: Enhance the current implementation to handle 10x load.",
            focus_area="Performance, Caching, Async Processing",
            difficulty="hard",
            rationale="High readiness demonstrates capability for advanced engineering challenges."
        ),
        borderline_task=TaskTemplate(
            title="Refactoring & Technical Debt Reduction",
            objective="Reinforcement Task: Improve code structure and address identified weaknesses.",
            focus_area="Clean Code, Error Handling, Validation",
            difficulty="medium",
            rationale="Foundational logic is sound but requires structural reinforcement."
        ),
        fail_task=TaskTemplate(
            title="Core Requirement Implementation",
            objective="Correction Task: Re-implement the missing core requirements.",
            focus_area="Basic Requirements, API Contract, Data Integrity",
            difficulty="easy",
            rationale="Critical requirements were missed. Focus on basics first."
        )
    )

    def generate_next_task(self, review: ReviewOutput, classification: str) -> V2NextTask:
        """
        Maps classification (PASS/BORDERLINE/FAIL) to a deterministic next task.
        """
        # Case-insensitive normalization
        status = classification.upper()
        
        if status == "PASS":
            template = self.RULES.pass_task
        elif status == "BORDERLINE":
            template = self.RULES.borderline_task
        else:
            # Default to FAIL logic for safety
            template = self.RULES.fail_task
            
        return V2NextTask(
            title=template.title,
            objective=template.objective,
            focus_area=template.focus_area,
            difficulty=template.difficulty
        )
