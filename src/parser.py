"""Document parsing using Docling."""

from pathlib import Path

from docling.document_converter import DocumentConverter

# Supported file extensions
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class ParserError(Exception):
    """Raised when document parsing fails."""

    pass


def parse_document(file_path: Path) -> str:
    """Parse a document and extract its text content.

    Args:
        file_path: Path to the document file (PDF, DOCX, or TXT)

    Returns:
        Extracted text content from the document

    Raises:
        ParserError: If the file doesn't exist, has unsupported format, or parsing fails
    """
    if not file_path.exists():
        raise ParserError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ParserError(
            f"Unsupported file format: {suffix}. "
            f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    # Handle plain text files directly
    if suffix == ".txt":
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Try with different encoding
            return file_path.read_text(encoding="latin-1")

    # Use Docling for PDF and DOCX
    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        return result.document.export_to_markdown()
    except Exception as e:
        raise ParserError(f"Failed to parse document: {e}") from e
