from .base import OutputFormatter, PromptResult


class JSONFormatter(OutputFormatter):
    def format(self, result: PromptResult) -> dict:
        return {
            "refined_prompt": result.refined,
            "original_prompt": result.original,
            "metadata": result.metadata,
        }
