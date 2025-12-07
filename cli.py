"""
Promptify CLI v1.0
Thin CLI layer - delegates to core modules
"""

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
from typing import Optional
import os

# Import core modules
from core.validator import InputValidator
from core.service import PromptifyService
from core.formatter import RichFormatter, JSONFormatter
from utils.errors import PromptifyError, ValidationError, ServiceError, ConfigurationError
from agent.graph import promptify

# Import CLI Helpers
from cli_supports.PromptifyTUI import PromptifyTUI

app = typer.Typer(
    name="promptify",
    help="🚀 Transform vague prompts into professional specs using AI agents",
    no_args_is_help=True
)
console = Console()

# Dependency injection
validator = InputValidator()
service = PromptifyService(graph=promptify)
formatters = {
    "rich": RichFormatter(),
    "json": JSONFormatter()
}


def show_banner():
    """Display banner"""
    try:
        from pyfiglet import Figlet
        fig = Figlet(font='slant')
        banner = fig.renderText('PROMPTIFY')
        console.print(f"[bold cyan]{banner}[/bold cyan]")
    except Exception:
        console.print("[bold cyan]╔═══════════════════════════╗[/bold cyan]")
        console.print("[bold cyan]║      PROMPTIFY v1.0       ║[/bold cyan]")
        console.print("[bold cyan]╚═══════════════════════════╝[/bold cyan]")
    console.print("[dim]Transform vague prompts → Professional specs[/dim]\n")


@app.command()
def refine(
    query: Optional[str] = typer.Argument(None, help="Query to refine"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read from file", exists=True),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Save to file"),
    format: str = typer.Option("tui", "--format", help="Output format: tui|rich|json"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed analysis")
):
    """
    Refine a prompt using AI agents
    
    Examples:
        promptify refine "build a chat app"
        promptify refine --file input.txt
        promptify refine "design database" --verbose
        promptify refine "build api" --format rich
        promptify refine "build api" --format json --output result.json
    """
    
    show_banner()
    
    try:
        # 1. Validate API key
        validator.validate_api_key(os.getenv("GOOGLE_GENAI_API_KEY"))
        
        # 2. Get and validate input
        if file:
            console.print(f"[dim]📁 Reading from: {file}[/dim]")
            query = validator.validate_file(file)
        else:
            query = validator.validate_query(query)
        
        # Show input
        console.print(f"[cyan]📝 Query:[/cyan] {query[:100]}{'...' if len(query) > 100 else ''}\n")
        
        # 3. Process with progress spinner
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("🤖 AI Agents working...", total=None)
            result = service.refine(query)
            progress.remove_task(task)
        
        console.print()
        console.print("[green]✅ Processing complete![/green]\n")
        
        result_text = result['final_prompt_draft']
        
        # 4. Display based on format
        if format == "tui":
            # Interactive TUI (default)
            tui = PromptifyTUI(result_text)
            tui.run()
        else:
            # Traditional CLI output (rich or json)
            formatter = formatters.get(format, formatters["rich"])
            output_text = formatter.format_result(result, verbose)
            
            if output_text:  # JSON returns string
                print(output_text)
        
        # 5. Save if requested
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(result_text, encoding='utf-8')
            console.print(f"\n✅ Saved to: [green]{output}[/green]")
        
        console.print("\n[dim]✨ Done![/dim]")
    
    except ValidationError as e:
        console.print(f"[red]❌ Validation Error:[/red]\n{e}")
        raise typer.Exit(1)
    
    except ConfigurationError as e:
        console.print(f"[red]❌ Configuration Error:[/red]\n{e}")
        raise typer.Exit(1)
    
    except ServiceError as e:
        console.print(f"[red]❌ Service Error:[/red]\n{e}")
        raise typer.Exit(1)
    
    except PromptifyError as e:
        console.print(f"[red]❌ Error:[/red]\n{e}")
        raise typer.Exit(1)
    
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Interrupted[/yellow]")
        raise typer.Exit(0)
    
    except Exception as e:
        console.print(f"[red]❌ Unexpected Error:[/red] {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def version():
    """Show version information"""
    show_banner()
    console.print("[bold]Version:[/bold] 1.0.0")
    console.print("[bold]Framework:[/bold] LangGraph + Gemini")
    console.print("[bold]Agents:[/bold] Triage → Critic → Expert → Smith")


if __name__ == "__main__":
    app()