"""
My-devin CLI Tool
Command-line interface for embedded systems development with LLM
"""

import sys
import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from src.llm.manager import LLMManager
from src.services.code_generator import CodeGenerator
from src.core.config import get_config

# Create Typer app
app = typer.Typer(
    name="my-devin",
    help="Local LLM-powered development platform for embedded systems",
    add_completion=False,
)

console = Console()


@app.command()
def chat(
    mode: str = typer.Option(
        "general",
        "--mode",
        "-m",
        help="Chat mode: general, embedded"
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        help="Override default model"
    ),
):
    """
    Interactive chat mode

    Example:
        my-devin chat
        my-devin chat --mode embedded
    """
    asyncio.run(_chat_async(mode, model))


async def _chat_async(mode: str, model: Optional[str]):
    """Async chat implementation"""

    config = get_config()
    llm = LLMManager(model_name=model) if model else LLMManager()

    # Check health
    console.print("[yellow]Connecting to LLM server...[/yellow]")
    is_healthy = await llm.health_check()

    if not is_healthy:
        console.print("[red]✗ LLM server is not available[/red]")
        console.print(f"[yellow]Please ensure LM Studio is running at {config.llm.lm_studio_base_url}[/yellow]")
        return

    console.print("[green]✓ Connected to LLM server[/green]")

    # Show mode
    mode_info = {
        "embedded": "🔧 Embedded Systems Development (C++/RTOS)",
        "general": "💻 General Software Development"
    }

    console.print(Panel(
        mode_info.get(mode, mode_info["general"]),
        title="My-devin Chat",
        border_style="blue"
    ))

    if mode == "embedded":
        console.print(f"[dim]Target: {config.embedded.target_mcu} | RTOS: {config.embedded.default_rtos}[/dim]")

    console.print("\n[dim]Type 'exit' or 'quit' to end the session[/dim]\n")

    # Chat loop
    while True:
        try:
            # Get user input
            user_input = console.input("[bold blue]You:[/bold blue] ").strip()

            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if not user_input:
                continue

            # Generate response
            console.print("[bold green]Assistant:[/bold green] ", end="")

            # Streaming response
            full_response = ""
            async for chunk in llm.stream_generate(user_input):
                console.print(chunk, end="", markup=False)
                full_response += chunk

            console.print("\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


@app.command()
def generate(
    description: str = typer.Argument(..., help="What code to generate"),
    language: str = typer.Option(
        "cpp",
        "--language",
        "-l",
        help="Programming language"
    ),
    rtos: Optional[str] = typer.Option(
        None,
        "--rtos",
        help="Target RTOS (freertos, zephyr, etc.)"
    ),
    target: Optional[str] = typer.Option(
        None,
        "--target",
        "-t",
        help="Target MCU (stm32f4, esp32, etc.)"
    ),
    peripheral: Optional[str] = typer.Option(
        None,
        "--peripheral",
        "-p",
        help="Peripheral type (uart, i2c, spi, etc.)"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path"
    ),
    embedded: bool = typer.Option(
        True,
        "--embedded/--no-embedded",
        help="Enable embedded mode for C/C++"
    ),
):
    """
    Generate code from description

    Examples:
        # FreeRTOS task
        my-devin generate "LED blink task" --language cpp --rtos freertos

        # UART driver
        my-devin generate "UART transmit function" --target stm32f4 --peripheral uart

        # Python code
        my-devin generate "binary search" --language python --no-embedded
    """
    asyncio.run(_generate_async(
        description, language, rtos, target, peripheral, output, embedded
    ))


async def _generate_async(
    description: str,
    language: str,
    rtos: Optional[str],
    target: Optional[str],
    peripheral: Optional[str],
    output: Optional[Path],
    embedded: bool,
):
    """Async code generation"""

    generator = CodeGenerator()

    # Show what we're generating
    info_lines = [f"[bold]Generating {language} code[/bold]"]
    if rtos:
        info_lines.append(f"RTOS: {rtos}")
    if target:
        info_lines.append(f"Target: {target}")
    if peripheral:
        info_lines.append(f"Peripheral: {peripheral}")

    console.print(Panel("\n".join(info_lines), border_style="blue"))

    # Generate code with progress spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating code...", total=None)

        try:
            code = await generator.generate(
                description=description,
                language=language,
                rtos=rtos,
                target=target,
                peripheral=peripheral,
                embedded=embedded,
            )

            progress.update(task, completed=True)

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error: {e}[/red]")
            return

    # Display generated code
    console.print(f"\n[bold green]Generated Code:[/bold green]\n")

    # Syntax highlighting
    from rich.syntax import Syntax

    syntax_lang = {
        "cpp": "cpp",
        "c": "c",
        "python": "python",
        "typescript": "typescript",
        "javascript": "javascript",
    }.get(language, language)

    syntax = Syntax(code, syntax_lang, theme="monokai", line_numbers=True)
    console.print(syntax)

    # Save to file if specified
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(code)
        console.print(f"\n[green]✓ Saved to {output}[/green]")


@app.command()
def analyze(
    path: Path = typer.Argument(..., help="Path to analyze"),
):
    """
    Analyze project structure

    Example:
        my-devin analyze ./my-project
    """
    console.print(f"[yellow]Analyzing: {path}[/yellow]")

    if not path.exists():
        console.print(f"[red]Error: Path does not exist: {path}[/red]")
        raise typer.Exit(1)

    # Basic analysis
    if path.is_file():
        console.print(f"[blue]File: {path.name}[/blue]")
        console.print(f"Size: {path.stat().st_size} bytes")

    elif path.is_dir():
        # Count files by extension
        extensions = {}
        total_files = 0

        for file in path.rglob("*"):
            if file.is_file():
                ext = file.suffix or "no extension"
                extensions[ext] = extensions.get(ext, 0) + 1
                total_files += 1

        console.print(Panel(
            f"[bold]Total Files:[/bold] {total_files}\n" +
            "\n".join(f"{ext}: {count}" for ext, count in sorted(extensions.items())),
            title=f"Project: {path.name}",
            border_style="blue"
        ))


@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
):
    """
    Configuration management

    Example:
        my-devin config --show
    """
    cfg = get_config()

    if show:
        console.print("[bold]My-devin Configuration[/bold]\n")

        console.print(Panel(
            f"Provider: {cfg.llm.provider}\n"
            f"Model: {cfg.llm.default_model}\n"
            f"LM Studio URL: {cfg.llm.lm_studio_base_url}",
            title="LLM Settings",
            border_style="blue"
        ))

        if cfg.is_embedded_mode():
            console.print(Panel(
                f"Enabled: {cfg.embedded.enabled}\n"
                f"Target MCU: {cfg.embedded.target_mcu}\n"
                f"Default RTOS: {cfg.embedded.default_rtos}\n"
                f"C++ Standard: {cfg.embedded.cpp_standard}\n"
                f"Optimization: {cfg.embedded.optimization}",
                title="Embedded Development",
                border_style="green"
            ))


@app.command()
def version():
    """Show version information"""
    console.print("[bold blue]My-devin[/bold blue] v0.1.0")
    console.print("Local LLM-powered development platform for embedded systems")


def main():
    """Entry point"""
    app()


if __name__ == "__main__":
    main()
