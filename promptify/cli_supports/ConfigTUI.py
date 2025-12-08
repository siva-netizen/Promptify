"""
Configuration TUI for Promptify
"""
import os
from pathlib import Path
from dotenv import set_key
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Grid
from textual.widgets import Header, Footer, Button, Static, Input, Select, Label
from textual.screen import Screen

from promptify.core.providerSelection.config import PromptifyConfig, MODEL_PRESETS

class ConfigTUI(App):
    """Interactive Configuration TUI"""
    
    CSS = """
    Screen {
        layout: vertical;
        padding: 1;
    }
    
    .box {
        height: auto;
        border: solid green;
        margin: 1;
        padding: 1;
    }
    
    Label {
        margin-top: 1;
        width: 100%; 
    }
    
    Select, Input {
        margin-bottom: 1;
    }
    
    #btn-bar {
        height: auto;
        dock: bottom;
        margin: 1;
        align: center middle;
    }
    
    Button {
        margin: 0 2;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.config = PromptifyConfig.load()
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Vertical(classes="box"):
            yield Label("Select Provider:")
            yield Select(
                [(p, p) for p in ["cerebras", "openai", "anthropic", "local"]],
                value=self.config.model.provider,
                id="provider-select"
            )
            
            yield Label("Model Name (Select preset or type custom):")
            # We'll use an Input for model to allow custom, but maybe a Select for common ones is better?
            # Let's stick to Input for flexibility, presetting it with current.
            yield Input(
                value=self.config.model.model,
                placeholder="e.g. gpt-4 or cerebras/llama3.1-8b",
                id="model-input"
            )
            
            yield Label("Temperature (0.0 - 1.0):")
            yield Input(
                value=str(self.config.model.temperature),
                id="temp-input"
            )
            
            yield Label("API Key (Updates .env):")
            yield Input(
                placeholder="Enter new API key to update (leave empty to keep current)",
                password=True,
                id="apikey-input"
            )
            
        with Horizontal(id="btn-bar"):
            yield Button("💾 Save & Exit", variant="success", id="save-btn")
            yield Button("❌ Cancel", variant="error", id="cancel-btn")
            
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-btn":
            self.save_config()
        elif event.button.id == "cancel-btn":
            self.exit()
            
    def save_config(self):
        # 1. Update Config Object
        provider = self.query_one("#provider-select", Select).value
        model = self.query_one("#model-input", Input).value
        temp_str = self.query_one("#temp-input", Input).value
        api_key = self.query_one("#apikey-input", Input).value
        
        try:
            self.config.model.provider = provider
            self.config.model.model = model
            self.config.model.temperature = float(temp_str)
            self.config.save()
            
            # 2. Update .env if API Key provided
            if api_key:
                env_path = Path(".env")
                if not env_path.exists():
                    env_path.touch()
                
                # Determine key name based on provider
                key_map = {
                    "cerebras": "CEREBRAS_API_KEY",
                    "openai": "OPENAI_API_KEY",
                    "anthropic": "ANTHROPIC_API_KEY",
                    "local": "LOCAL_API_KEY" # Generic
                }
                env_var = key_map.get(provider, "LLM_API_KEY")
                
                # Use python-dotenv to set key
                set_key(env_path, env_var, api_key)
                
            self.exit(result="Saved")
            print(f"✅ Configuration saved! Provider: {provider}, Model: {model}")
            
        except ValueError:
            self.notify("Invalid Temperature!", severity="error")
        except Exception as e:
            self.notify(f"Error saving: {e}", severity="error")
