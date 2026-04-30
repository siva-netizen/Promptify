from .base import OutputFormatter, PromptResult


class ToonFormatter(OutputFormatter):
    def format(self, result: PromptResult) -> str:
        try:
            from toon_format import encode
        except ImportError as e:
            raise ImportError("toon-format is required: uv add toon-format") from e

        data = {
            "refined_prompt": result.refined,
            "original_prompt": result.original,
            "metadata": result.metadata,
        }
        return encode(data)
