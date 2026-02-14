from ..core.interfaces.next_task_interface import NextTaskGeneratorInterface
from ..models.schemas import ReviewOutput, NextTask
from .next_task_engine import NextTaskEngine

class NextTaskAdapter(NextTaskGeneratorInterface):
    def generate_next_task(self, review: ReviewOutput, classification: str) -> NextTask:
        # The existing engine doesn't use explicit classification, but we adhere to the interface
        return NextTaskEngine.generate_next_task(review)
