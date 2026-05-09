import json
from .base import OutputFormatter, PromptResult


class JSONFormatter(OutputFormatter):
    def format(self, result: PromptResult) -> str:
        return json.dumps({
            "refined_prompt": result.refined,
            "original_prompt": result.original,
            "metadata": result.metadata,
        }, indent=2)
