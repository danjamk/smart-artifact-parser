# Smart Medical Document Parser - Implementation Plan

## Overview
A CLI tool that extracts structured medical information from documents (PDF, DOCX, TXT) using Docling for parsing and Claude for intelligent extraction.

## Tech Stack
- **Python 3.12**
- **Docling** - Document parsing
- **Anthropic Claude (Sonnet)** - LLM extraction
- **Pydantic** - Schema validation
- **Typer** - CLI interface
- **uv** - Package management

## Project Structure
```
smart-artifact-parser/
├── src/
│   ├── __init__.py
│   ├── parser.py        # Document parsing (Docling)
│   ├── extractor.py     # LLM extraction logic
│   ├── schemas.py       # Pydantic models for medical data
│   └── cli.py           # Command-line interface
├── samples/             # Sample documents for testing
├── output/              # Default output directory
├── pyproject.toml
├── .env.example
├── CLAUDE.md
└── README.md
```

---

## Phase 1: Core Extraction (COMPLETED)

### Step 1: Project Setup ✅
- [x] Create `pyproject.toml` with dependencies (docling, anthropic, pydantic, typer, python-dotenv)
- [x] Create `.env.example` with `ANTHROPIC_API_KEY=your_key_here`
- [x] Create `output/` directory with `.gitkeep`
- [x] Configure hatchling build for `src/` package

### Step 2: Define Pydantic Schemas (`src/schemas.py`) ✅
Initial schema (lean MVP):
- [x] `Provider` - name, specialty, facility
- [x] `Diagnosis` - description, icd_code
- [x] `Medication` - name, dosage, frequency, instructions
- [x] `MedicalDocumentExtraction` - extraction schema for Claude
- [x] `MedicalDocument` - full model with metadata (raw_text, source_file, extracted_at)

### Step 3: Document Parser (`src/parser.py`) ✅
- [x] Create `parse_document(file_path: Path) -> str` function
- [x] Use Docling to handle PDF, DOCX
- [x] Direct read for TXT files
- [x] Error handling with custom `ParserError`

### Step 4: LLM Extractor (`src/extractor.py`) ✅
- [x] Create `extract_medical_info()` function
- [x] System prompt for medical document analysis
- [x] Claude tool_use with Pydantic schema for structured output
- [x] API error handling

### Step 5: CLI Interface (`src/cli.py`) ✅
- [x] Typer app with `extract` command
- [x] Arguments: `file_path` (required), `--output-dir` (optional)
- [x] Load API key from `.env`
- [x] Output filename: `{base_name}_{timestamp}.json`
- [x] Progress display and extraction summary

### Step 6: Testing ✅
- [x] Tested with sample TXT file
- [x] Tested with PDF documents
- [x] All document types working

---

## Current Schema

```python
MedicalDocument:
  - document_type: visit_note | lab_result | discharge_summary | prescription | referral | imaging_report | other
  - document_date: date | None
  - provider: Provider | None
  - chief_complaint: str | None
  - assessment: str | None
  - diagnoses: list[Diagnosis]
  - medications: list[Medication]
  - follow_up_instructions: str | None
  - raw_text: str
  - source_file: str
  - extracted_at: datetime
```

---

## CLI Usage
```bash
# Install dependencies
uv sync

# Set up API key
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Extract from a document
uv run python -m src.cli /path/to/document.pdf

# Specify output directory
uv run python -m src.cli /path/to/document.pdf --output-dir ./my_records
```

---

## Phase 2: Schema Expansion (PLANNED)

Entities to add:
- [ ] `Patient` - name, date_of_birth, medical_record_number
- [ ] `Vitals` - blood_pressure, heart_rate, temperature, weight, height, oxygen_saturation
- [ ] `LabResult` - test_name, value, units, reference_range, flag
- [ ] `Allergy` - allergen, reaction, severity
- [ ] `Procedure` - name, cpt_code, date

---

## Phase 3: Storage & RAG (PLANNED)

- [ ] ChromaDB integration for vector storage
- [ ] Store raw_text with embeddings for semantic search
- [ ] SQLite/PostgreSQL for structured data persistence
- [ ] Query interface across documents

---

## Phase 4: Additional Features (PLANNED)

- [ ] Batch processing mode
- [ ] OCR support for scanned documents
- [ ] Web interface
- [ ] Export to FHIR format
