from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process the input data and return a result dictionary.
        """
        pass
