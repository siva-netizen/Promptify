import json
from .base import OutputFormatter, PromptResult


class MarkdownFormatter(OutputFormatter):
    def format(self, result: PromptResult) -> str:
        return (
            f"## Refined Prompt\n{result.refined}\n\n"
            f"## Original\n{result.original}\n\n"
            f"## Metadata\n```json\n{json.dumps(result.metadata, indent=2)}\n```"
        )
