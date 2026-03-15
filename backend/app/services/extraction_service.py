from collections.abc import Sequence

from app.schemas.common import Warning
from app.schemas.extraction import ExtractionResponse
from app.schemas.insurance import Insurance
from app.schemas.patient import Patient
from app.services.normalization_service import normalize_insurance, normalize_patient
from app.services.storage_service import StoredDocument


def extract_from_documents(documents: Sequence[StoredDocument]) -> ExtractionResponse:
  patient = normalize_patient(
      Patient(
          first_name="Avery",
          middle_name="Jordan",
          last_name="Carter",
          date_of_birth="1988-11-04",
          address="123 Harbor Street",
          city="Baltimore",
          state="md",
          postal_code="21201",
      )
  )
  insurance = normalize_insurance(
      Insurance(
          payer_name="Blue Cross Blue Shield of Maryland",
          payer_id="bcbsmd01",
          member_id="xjh123456789",
          group_number="grp-45029",
          rx_bin="610279",
          rx_pcn="03200000",
          rx_group="mdrx01",
      )
  )

  document_notes = [
      f"{document.document_type} saved from {document.original_filename}"
      for document in documents
  ]

  warnings = [
      Warning(
          code="OCR-MOCK",
          message="Prototype extraction is returning fixture-based data until OCR is added.",
          severity="info",
      ),
      Warning(
          code="REVIEW-REQUIRED",
          message="Please verify payer ID and group number against the uploaded card images.",
          severity="warning",
      ),
  ]

  return ExtractionResponse(
      patient=patient,
      insurance=insurance,
      confidence=0.93,
      document_notes=document_notes,
      warnings=warnings,
  )
