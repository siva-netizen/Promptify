from .registry import FormatterRegistry
from .json_formatter import JSONFormatter
from .markdown_formatter import MarkdownFormatter
from .toon_formatter import ToonFormatter

FormatterRegistry.register("json", JSONFormatter())
FormatterRegistry.register("markdown", MarkdownFormatter())
FormatterRegistry.register("toon", ToonFormatter())

__all__ = ["FormatterRegistry"]
