# Smart Artifact Parser

Medical document extraction tool using Docling and Claude AI.

## Project Structure

```
src/
├── cli.py          # Typer CLI - entry point
├── parser.py       # Docling document parsing (PDF, DOCX, TXT)
├── extractor.py    # Claude API for structured extraction
└── schemas.py      # Pydantic models for medical data
```

## Quick Commands

```bash
# Run extraction
uv run python -m src.cli <document_path>

# With custom output directory
uv run python -m src.cli <document_path> --output-dir ./my_output

# Install dependencies
uv sync
```

## Environment Setup

Requires `ANTHROPIC_API_KEY` in `.env` file.

## Key Files

- `src/schemas.py` - Define extraction schema here. `MedicalDocumentExtraction` is sent to Claude, `MedicalDocument` adds metadata.
- `src/extractor.py` - System prompt and Claude API call. Uses tool_use for structured output.
- `src/parser.py` - Handles PDF/DOCX via Docling, TXT directly.

## Supported Document Types

- PDF (via Docling)
- DOCX (via Docling)
- TXT (direct read)

## Output

JSON files saved to `output/` with naming: `{filename}_{timestamp}.json`

## Extending the Schema

1. Add new Pydantic models to `src/schemas.py`
2. Add fields to `MedicalDocumentExtraction`
3. Claude will automatically extract the new fields

## Architecture Notes

- Uses Claude's tool_use feature with Pydantic schema for reliable structured output
- Docling converts documents to markdown, preserving tables and structure
- All extracted data validated through Pydantic before output
