"""
Promptify CLI v1.0 with Interactive TUI
"""
import pyperclip

# Textual imports
from textual.app import App, ComposeResult
from textual.containers import  Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, TextArea
from textual.binding import Binding

class PromptifyTUI(App):
    """Interactive Promptify TUI with copy button"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #result-container {
        height: 100%;
        border: solid $primary;
        margin: 1;
    }
    
    #result-text {
        height: 1fr;
        background: $surface-darken-1;
        padding: 1;
    }
    
    #button-bar {
        height: auto;
        dock: bottom;
        background: $panel;
        padding: 1;
    }
    
    Button {
        margin: 0 1;
    }
    
    .success {
        background: $success;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("c", "copy", "Copy"),
    ]
    
    def __init__(self, result_text: str):
        super().__init__()
        self.result_text = result_text
        self.copied = False
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="result-container"):
            yield Static("* PROMPTIFIED ", id="title")
            yield TextArea(
                self.result_text,
                id="result-text",
                read_only=True,
                show_line_numbers=False
            )
            with Horizontal(id="button-bar"):
                yield Button("Copy", variant="primary", id="copy-btn")
                yield Button("✖ Close", variant="error", id="close-btn")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "copy-btn":
            self.action_copy()
        elif event.button.id == "close-btn":
            self.exit()
    
    def action_copy(self) -> None:
        """Copy result to clipboard"""
        try:
            pyperclip.copy(self.result_text)
            self.notify("✔ Copied to clipboard!", severity="information")
            self.copied = True
        except Exception as e:
            self.notify(f"✖ Copy failed: {e}", severity="error")
    
