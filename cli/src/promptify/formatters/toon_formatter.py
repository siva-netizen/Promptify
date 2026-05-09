from .base import OutputFormatter, PromptResult


class ToonFormatter(OutputFormatter):
    def format(self, result: PromptResult) -> str:
        try:
            import toons
        except ImportError as e:
            raise ImportError("toons is required: pip install toons") from e

        data = {
            "refined_prompt": result.refined,
            "original_prompt": result.original,
            "metadata": result.metadata,
        }
        return toons.dumps(data)
