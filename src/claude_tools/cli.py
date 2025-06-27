"""Command-line interface for Claude Smart Tools."""
import click
from claude_tools import __version__


@click.group()
@click.version_option(version=__version__, prog_name="claude-tools")
def main():
    """Claude Smart Tools - A collection of reusable tools."""
    pass


@main.command()
def list():
    """List all available tools."""
    click.echo("Available tools:")
    click.echo("  - example_tool: Demonstrates the tool framework")
    # Add more tools as they are created


if __name__ == "__main__":
    main()