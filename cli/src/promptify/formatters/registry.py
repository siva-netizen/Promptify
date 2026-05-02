from .base import OutputFormatter, PromptResult


class FormatterRegistry:
    _formatters: dict[str, OutputFormatter] = {}

    @classmethod
    def register(cls, name: str, formatter: OutputFormatter) -> None:
        cls._formatters[name] = formatter

    @classmethod
    def format(cls, name: str, result: PromptResult) -> str | dict:
        formatter = cls._formatters.get(name)
        if not formatter:
            raise ValueError(f"Unknown format: '{name}'. Registered: {list(cls._formatters)}")
        return formatter.format(result)

    @classmethod
    def list_formats(cls) -> list[str]:
        return list(cls._formatters.keys())
