"""Pydantic schemas for medical document extraction."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class Provider(BaseModel):
    """Healthcare provider information."""

    name: str = Field(description="Full name of the healthcare provider")
    specialty: str | None = Field(
        default=None, description="Medical specialty (e.g., Internal Medicine, Cardiology)"
    )
    facility: str | None = Field(
        default=None, description="Name of the medical facility or practice"
    )


class Diagnosis(BaseModel):
    """A medical diagnosis."""

    description: str = Field(description="Description of the diagnosis")
    icd_code: str | None = Field(
        default=None, description="ICD-10 code if mentioned in the document"
    )


class Medication(BaseModel):
    """A prescribed or mentioned medication."""

    name: str = Field(description="Name of the medication")
    dosage: str | None = Field(default=None, description="Dosage amount (e.g., 500mg, 10ml)")
    frequency: str | None = Field(
        default=None, description="How often to take (e.g., twice daily, as needed)"
    )
    instructions: str | None = Field(
        default=None, description="Additional instructions (e.g., take with food)"
    )


class MedicalDocumentExtraction(BaseModel):
    """Extracted medical information from a document.

    This schema is used for LLM extraction - it contains only the fields
    that should be extracted from the document text.
    """

    document_type: Literal[
        "visit_note",
        "lab_result",
        "discharge_summary",
        "prescription",
        "referral",
        "imaging_report",
        "other",
    ] = Field(description="Type of medical document")

    document_date: date | None = Field(
        default=None, description="Date of the visit or document"
    )

    provider: Provider | None = Field(
        default=None, description="Healthcare provider information"
    )

    chief_complaint: str | None = Field(
        default=None, description="Primary reason for the visit or main concern"
    )

    assessment: str | None = Field(
        default=None, description="Provider's assessment or clinical impression"
    )

    diagnoses: list[Diagnosis] = Field(
        default_factory=list, description="List of diagnoses mentioned"
    )

    medications: list[Medication] = Field(
        default_factory=list, description="List of medications prescribed or mentioned"
    )

    follow_up_instructions: str | None = Field(
        default=None, description="Follow-up care instructions"
    )


class MedicalDocument(MedicalDocumentExtraction):
    """Complete medical document record including metadata.

    Extends the extraction schema with metadata fields that are added
    after extraction (source file, timestamp, raw text).
    """

    raw_text: str = Field(description="Original extracted text from the document")
    source_file: str = Field(description="Original filename")
    extracted_at: datetime = Field(description="Timestamp of extraction")
