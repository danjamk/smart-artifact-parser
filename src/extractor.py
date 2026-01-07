"""LLM-based medical information extraction using Claude."""

import json
from datetime import datetime

import anthropic

from .schemas import MedicalDocument, MedicalDocumentExtraction

SYSTEM_PROMPT = """You are a medical document analyst. Your task is to extract structured information from medical documents.

Guidelines:
- Extract only information that is explicitly stated in the document
- Do not infer or assume information that isn't present
- If a field cannot be determined from the document, leave it as null
- For dates, use ISO format (YYYY-MM-DD)
- For ICD codes, only include if explicitly mentioned
- Be precise with medication dosages and frequencies as written
- Preserve medical terminology as used in the document

Document types:
- visit_note: Office visit, consultation, or clinical encounter notes
- lab_result: Laboratory test results
- discharge_summary: Hospital discharge documentation
- prescription: Medication prescriptions
- referral: Referral letters to specialists
- imaging_report: X-ray, MRI, CT scan reports
- other: Any other medical document type"""

USER_PROMPT_TEMPLATE = """Extract the medical information from the following document.

<document>
{text}
</document>

Extract all relevant medical information according to the schema provided."""


class ExtractorError(Exception):
    """Raised when extraction fails."""

    pass


def extract_medical_info(
    text: str,
    source_file: str,
    api_key: str,
    model: str = "claude-sonnet-4-20250514",
) -> MedicalDocument:
    """Extract medical information from document text using Claude.

    Args:
        text: The document text to analyze
        source_file: Original filename for metadata
        api_key: Anthropic API key
        model: Claude model to use

    Returns:
        MedicalDocument with extracted information

    Raises:
        ExtractorError: If extraction fails
    """
    client = anthropic.Anthropic(api_key=api_key)

    # Build the extraction tool from the Pydantic schema
    extraction_tool = {
        "name": "extract_medical_info",
        "description": "Extract structured medical information from a document",
        "input_schema": MedicalDocumentExtraction.model_json_schema(),
    }

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=[extraction_tool],
            tool_choice={"type": "tool", "name": "extract_medical_info"},
            messages=[
                {
                    "role": "user",
                    "content": USER_PROMPT_TEMPLATE.format(text=text),
                }
            ],
        )

        # Extract the tool use result
        for block in response.content:
            if block.type == "tool_use" and block.name == "extract_medical_info":
                extracted_data = block.input

                # Create the full document with metadata
                return MedicalDocument(
                    **extracted_data,
                    raw_text=text,
                    source_file=source_file,
                    extracted_at=datetime.now(),
                )

        raise ExtractorError("No extraction result in response")

    except anthropic.APIError as e:
        raise ExtractorError(f"API error: {e}") from e
    except json.JSONDecodeError as e:
        raise ExtractorError(f"Failed to parse extraction result: {e}") from e
