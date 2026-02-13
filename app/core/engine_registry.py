from ..services.review_engine import ReviewEngine
from ..core.interfaces.review_engine_interface import ReviewEngineInterface

class EngineRegistry:
    _engine: ReviewEngineInterface = ReviewEngine()

    @classmethod
    def get_engine(cls) -> ReviewEngineInterface:
        return cls._engine

    @classmethod
    def register_engine(cls, engine: ReviewEngineInterface):
        cls._engine = engine
