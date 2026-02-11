from typing import Dict, Any
from collections import OrderedDict
from .schemas import Task

# Memory Locked Storage: Cap at 1000 tasks to prevent memory pressure during demo
class LimitedStorage(OrderedDict):
    def __init__(self, limit: int = 1000):
        self.limit = limit
        super().__init__()

    def __setitem__(self, key: str, value: Any):
        if len(self) >= self.limit:
            self.popitem(last=False)  # Evict oldest entry (FIFO)
        super().__setitem__(key, value)

task_storage = LimitedStorage(limit=1000)
