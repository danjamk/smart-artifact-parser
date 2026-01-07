"""Command-line interface for the medical document parser."""

import json
import os
from datetime import datetime
from pathlib import Path

import typer
from dotenv import load_dotenv

from .extractor import ExtractorError, extract_medical_info
from .parser import ParserError, parse_document

app = typer.Typer(
    name="smart-parser",
    help="Extract structured medical information from documents.",
    no_args_is_help=True,
)


def generate_output_filename(source_file: Path) -> str:
    """Generate output filename with timestamp.

    Args:
        source_file: Original source file path

    Returns:
        Filename in format: {base_name}_{timestamp}.json
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{source_file.stem}_{timestamp}.json"


@app.command()
def extract(
    file_path: Path = typer.Argument(
        ...,
        help="Path to the document to process (PDF, DOCX, or TXT)",
        exists=True,
        readable=True,
    ),
    output_dir: Path = typer.Option(
        Path("output"),
        "--output-dir",
        "-o",
        help="Directory to save extracted JSON",
    ),
) -> None:
    """Extract medical information from a document."""
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        typer.secho(
            "Error: ANTHROPIC_API_KEY not found. "
            "Please set it in .env file or environment.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Processing: {file_path.name}")

    # Step 1: Parse the document
    typer.echo("  Parsing document...")
    try:
        text = parse_document(file_path)
    except ParserError as e:
        typer.secho(f"  Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.echo(f"  Extracted {len(text):,} characters")

    # Step 2: Extract medical information
    typer.echo("  Extracting medical information...")
    try:
        result = extract_medical_info(
            text=text,
            source_file=file_path.name,
            api_key=api_key,
        )
    except ExtractorError as e:
        typer.secho(f"  Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Step 3: Save results
    output_filename = generate_output_filename(file_path)
    output_path = output_dir / output_filename

    output_path.write_text(
        result.model_dump_json(indent=2),
        encoding="utf-8",
    )

    typer.secho(f"  Saved to: {output_path}", fg=typer.colors.GREEN)

    # Display summary
    typer.echo("\nExtraction Summary:")
    typer.echo(f"  Document type: {result.document_type}")
    if result.document_date:
        typer.echo(f"  Date: {result.document_date}")
    if result.provider:
        typer.echo(f"  Provider: {result.provider.name}")
    if result.diagnoses:
        typer.echo(f"  Diagnoses: {len(result.diagnoses)}")
    if result.medications:
        typer.echo(f"  Medications: {len(result.medications)}")


if __name__ == "__main__":
    app()
