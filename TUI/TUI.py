import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional
from pathlib import Path

from agent.graph import promptify

# Initialize
app = typer.Typer(
    name="promptify",
    help="🚀 AI-powered prompt engineering tool that transforms vague queries into structured prompts",
    add_completion=False
)
console = Console()

@app.command()
def refine(
    query: Optional[str] = typer.Argument(None, help="The query to refine"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read query from file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Save result to file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed analysis"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy result to clipboard")
):
    """
    Refine a prompt using AI agents (Triage → Critic → Expert → Smith)
    
    Examples:
        promptify refine "build a chat app"
        promptify refine --file input.txt --output result.txt
        promptify refine "explain transformers" --verbose
    """
    
    # Get input
    if file:
        query = file.read_text()
    elif not query:
        query = typer.prompt("📝 Enter your query")
    
    # Initialize state
    initial_state = {
        "user_query": query,
        "intent": "",
        "critique": None,
        "expert_suggestions": "",
        "final_prompt_draft": "",
        "iteration_count": 0
    }
    
    # Show input
    console.print(Panel(f"[cyan]{query}[/cyan]", title="📝 Original Query", border_style="cyan"))
    
    # Run with progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("🤖 AI Agents working...", total=None)
        result = promptify.invoke(initial_state)
        progress.update(task, completed=True)
    
    # Display results
    console.print(Panel(
        f"[bold green]{result['intent']}[/bold green]",
        title="🎯 Detected Intent",
        border_style="green"
    ))
    
    if verbose:
        console.print(Panel(
            result['critique'],
            title="🔍 Critique",
            border_style="yellow"
        ))
        console.print(Panel(
            result['expert_suggestions'],
            title="💡 Expert Suggestions",
            border_style="blue"
        ))
    
    # Final output
    final_prompt = result['final_prompt_draft']
    console.print(Panel(
        f"[bold white]{final_prompt}[/bold white]",
        title="✨ Refined Prompt",
        border_style="magenta"
    ))
    
    # Save to file
    if output:
        output.write_text(final_prompt)
        console.print(f"✅ Saved to: [green]{output}[/green]")
    
    # Copy to clipboard
    if copy:
        try:
            import pyperclip
            pyperclip.copy(final_prompt)
            console.print("📋 Copied to clipboard!")
        except ImportError:
            console.print("[yellow]Install 'pyperclip' to enable clipboard support[/yellow]")


@app.command()
def interactive():
    """
    Interactive mode - refine multiple prompts in a session
    """
    console.print(Panel(
        "[bold cyan]Promptify Interactive Mode[/bold cyan]\n"
        "Type your queries. Type 'exit' or 'quit' to leave.",
        border_style="cyan"
    ))
    
    while True:
        try:
            query = typer.prompt("\n📝 Query (or 'exit')")
            if query.lower() in ['exit', 'quit', 'q']:
                console.print("👋 Goodbye!")
                break
            
            initial_state = {
                "user_query": query,
                "intent": "",
                "critique": None,
                "expert_suggestions": "",
                "final_prompt_draft": "",
                "iteration_count": 0
            }
            
            with console.status("[bold green]Processing..."):
                result = promptify.invoke(initial_state)
            
            console.print(Panel(
                result['final_prompt_draft'],
                title=f"✨ Refined [{result['intent']}]",
                border_style="magenta"
            ))
            
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!")
            break


@app.command()
def version():
    """Show Promptify version"""
    console.print("[bold cyan]Promptify[/bold cyan] v1.0.0")


if __name__ == "__main__":
    app()
