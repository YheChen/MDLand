from datetime import datetime

from app.schemas.common import APIModel, Warning
from app.schemas.insurance import Insurance
from app.schemas.patient import Patient
from app.schemas.summary import VerificationSummary


class VerificationRequest(APIModel):
  patient: Patient
  insurance: Insurance


class VerificationResponse(APIModel):
  summary: VerificationSummary
  warnings: list[Warning]
  raw_271: str
  checked_at: datetime
