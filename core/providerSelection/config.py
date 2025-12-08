"""
Configuration using provider registry
"""

from pathlib import Path
from typing import Optional, Literal
import yaml
from pydantic import BaseModel, Field

ProviderType = Literal["cerebras", "openai", "anthropic", "local"]
MODEL_PRESETS = {
    # Cerebras (DEFAULT - free tier)
    "default": {"provider": "cerebras", "model": "cerebras/llama3.1-8b"},
    "cerebras-8b": {"provider": "cerebras", "model": "cerebras/llama3.1-8b"},
    "cerebras-70b": {"provider": "cerebras", "model": "cerebras/llama-3.3-70b"},
    
    # OpenAI
    "gpt-4o": {"provider": "openai", "model": "gpt-4o"},
    "gpt-3.5": {"provider": "openai", "model": "gpt-3.5-turbo"},
    
    # Anthropic
    "claude": {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
}

class ModelConfig(BaseModel):
    """Model configuration"""
    provider: ProviderType = "cerebras"  # DEFAULT: Cerebras (free tier)
    model: str = "cerebras/llama3.1-8b"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    # For local/custom endpoints
    api_base: Optional[str] = None
    api_key: Optional[str] = None


class PromptifyConfig(BaseModel):
    """Main config"""
    model: ModelConfig = Field(default_factory=ModelConfig)
    verbose: bool = False
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "PromptifyConfig":
        # Load environment variables from .env if present
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass # dotenv not installed, hopefully env vars are set otherwise

        if config_path is not None:
             if config_path.exists():
                with open(config_path) as f:
                    data = yaml.safe_load(f) or {}
                return cls(**data)
             return cls()

        # Search order: local first, then global
        paths = [
            Path("config.yml"),
            Path("config.yaml"),
            Path.home() / ".promptify" / "config.yml",
            Path.home() / ".promptify" / "config.yaml"
        ]

        for path in paths:
            if path.exists():
                with open(path) as f:
                    data = yaml.safe_load(f) or {}
                return cls(**data)
        
        return cls()  # Default: Cerebras free tier
    
    def save(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path.home() / ".promptify" / "config.yaml"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(self.model_dump(), f)