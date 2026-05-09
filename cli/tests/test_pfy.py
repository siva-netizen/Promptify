"""Unit tests for pfy package — no LLM calls required"""
import pytest
from unittest.mock import MagicMock

from promptify.utils.errors import (
    ServiceError, ValidationError, ConfigurationError, APIError,
    rate_limit_error, network_error, api_key_missing_error, query_too_long_error,
)
from promptify.formatters import FormatterRegistry
from promptify.formatters.base import PromptResult
from promptify.core.service import PromptifyService


# --- Errors ---

def test_service_error_with_hint():
    e = ServiceError("failed", hint="try again")
    assert "failed" in str(e)
    assert "try again" in str(e)

def test_api_error_status_code():
    e = APIError("bad request", status_code=400)
    assert "400" in str(e)

def test_rate_limit_error():
    e = rate_limit_error()
    assert e.status_code == 429

def test_network_error():
    e = network_error()
    assert "Network error" in str(e)

def test_api_key_missing_error():
    e = api_key_missing_error()
    assert isinstance(e, ConfigurationError)

def test_query_too_long_error():
    e = query_too_long_error(6000)
    assert isinstance(e, ValidationError)
    assert "6000" in str(e)


# --- Formatters ---

def test_formatter_registry_lists_formats():
    formats = FormatterRegistry.list_formats()
    assert "json" in formats
    assert "markdown" in formats
    assert "toon" in formats

def test_unknown_format_raises():
    result = PromptResult(original="x", refined="y")
    with pytest.raises(ValueError, match="Unknown format"):
        FormatterRegistry.format("nonexistent", result)

def test_json_formatter():
    result = PromptResult(original="hello", refined="world", metadata={"k": "v"})
    output = FormatterRegistry.format("json", result)
    assert isinstance(output, (str, dict))

def test_markdown_formatter():
    result = PromptResult(original="hello", refined="world")
    output = FormatterRegistry.format("markdown", result)
    assert isinstance(output, str)
    assert "world" in output


# --- PromptifyService ---

def test_service_refine_returns_state():
    mock_graph = MagicMock()
    mock_graph.invoke.return_value = {
        "final_prompt_draft": "refined output",
        "iteration_count": 2,
    }
    svc = PromptifyService(graph=mock_graph)
    result = svc.refine("test query")
    assert result["final_prompt_draft"] == "refined output"
    mock_graph.invoke.assert_called_once()

def test_service_refine_with_output_format():
    mock_graph = MagicMock()
    mock_graph.invoke.return_value = {
        "final_prompt_draft": "refined output",
        "iteration_count": 1,
    }
    svc = PromptifyService(graph=mock_graph)
    result = svc.refine("test query", output_format="markdown")
    assert isinstance(result, str)
    assert "refined output" in result

def test_service_wraps_rate_limit_error():
    mock_graph = MagicMock()
    mock_graph.invoke.side_effect = Exception("429 rate limit exceeded")
    svc = PromptifyService(graph=mock_graph)
    with pytest.raises(APIError):
        svc.refine("test")

def test_service_wraps_generic_error():
    mock_graph = MagicMock()
    mock_graph.invoke.side_effect = Exception("something unexpected")
    svc = PromptifyService(graph=mock_graph)
    with pytest.raises(ServiceError):
        svc.refine("test")
