from app.schemas.common import APIModel, Warning
from app.schemas.insurance import Insurance
from app.schemas.patient import Patient


class ExtractionResponse(APIModel):
  patient: Patient
  insurance: Insurance
  confidence: float
  document_notes: list[str]
  warnings: list[Warning] = []
