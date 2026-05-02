from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PromptResult:
    original: str
    refined: str
    metadata: dict[str, Any] = field(default_factory=dict)


class OutputFormatter(ABC):
    @abstractmethod
    def format(self, result: PromptResult) -> str | dict:
        ...
