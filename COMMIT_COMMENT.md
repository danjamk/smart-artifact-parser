# Commit Message

```
Add medical document extraction CLI tool

Implement Phase 1 of smart-artifact-parser: a CLI tool that extracts
structured medical information from PDF, DOCX, and TXT documents using
Docling for parsing and Claude (Sonnet) for intelligent extraction.

Features:
- Document parsing via Docling with support for PDF, DOCX, TXT
- Structured extraction using Claude's tool_use with Pydantic schemas
- Extracts: document type, date, provider, diagnoses (with ICD codes),
  medications, chief complaint, assessment, and follow-up instructions
- Typer CLI with progress display and extraction summary
- JSON output with timestamped filenames

Tech stack: Python 3.12, Docling, Anthropic API, Pydantic, Typer, uv

Usage: uv run python -m src.cli <document_path>
```
