"""Command-line interface for Claude Smart Tools."""

import click

from claude_tools import __version__
from claude_tools.tools.image_upscaler import ImageUpscaler


@click.group()
@click.version_option(version=__version__, prog_name="claude-tools")
def main() -> None:
    """Claude Smart Tools - A collection of reusable tools."""
    pass


@main.command()
def list() -> None:
    """List all available tools."""
    click.echo("Available tools:")
    click.echo("  - example_tool: Demonstrates the tool framework")
    click.echo("  - upscale: AI-powered image upscaler for maximum quality")


@main.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output path (default: auto-generated)",
)
@click.option(
    "--scale", "-s", type=float, default=4.0, help="Scale factor (default: 4.0)"
)
@click.option(
    "--method",
    "-m",
    type=click.Choice(["auto", "ai", "fallback"]),
    default="auto",
    help="Upscaling method (default: auto)",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def upscale(
    input_path: str, output: str, scale: float, method: str, verbose: bool
) -> None:
    """Upscale an image using AI or classical methods.

    INPUT_PATH: Path to the input image file

    Examples:
        claude-tools upscale image.jpg --scale 2.0
        claude-tools upscale logo.png -o big_logo.png --method ai
        claude-tools upscale photo.jpg --scale 4.0 --verbose
    """
    try:
        if verbose:
            click.echo(f"Upscaling {input_path} by {scale}x using {method} method...")

        upscaler = ImageUpscaler()

        # Prepare arguments
        kwargs = {
            "input_path": input_path,
            "scale_factor": scale,
            "method": method,
        }

        if output:
            kwargs["output_path"] = output

        # Execute upscaling
        result = upscaler.execute(**kwargs)

        if result.get("success", False):
            click.echo(f"✅ Success! Upscaled to: {result['output_path']}")

            if verbose:
                click.echo(f"   Method used: {result['method_used']}")
                click.echo(
                    f"   Original size: {result['original_dimensions'][0]}x{result['original_dimensions'][1]}"
                )
                click.echo(
                    f"   New size: {result['upscaled_dimensions'][0]}x{result['upscaled_dimensions'][1]}"
                )
                click.echo(
                    f"   File size: {result['file_size_before']} → {result['file_size_after']} bytes"
                )

        else:
            click.echo(f"❌ Failed: {result.get('error', 'Unknown error')}", err=True)
            raise click.ClickException("Upscaling failed")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.ClickException(str(e)) from e


if __name__ == "__main__":
    main()
