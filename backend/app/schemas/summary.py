from app.schemas.common import APIModel, CoverageStatus, VerificationStatus


class Discrepancy(APIModel):
  field: str
  extracted_value: str
  verified_value: str
  note: str


class CopaySummary(APIModel):
  primary_care: str
  specialist: str
  urgent_care: str
  pharmacy: str


class PharmacyInfo(APIModel):
  bin: str
  pcn: str
  group: str
  processor: str


class VerificationSummary(APIModel):
  verification_status: VerificationStatus
  coverage_status: CoverageStatus
  payer_name: str
  member_id: str
  copays: CopaySummary
  pharmacy_info: PharmacyInfo
  discrepancies: list[Discrepancy]
