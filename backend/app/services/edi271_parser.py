from dataclasses import dataclass

from app.schemas.common import CoverageStatus, VerificationStatus, Warning
from app.schemas.patient import Patient
from app.schemas.summary import CopaySummary, PharmacyInfo


@dataclass
class Parsed271:
  verification_status: VerificationStatus
  coverage_status: CoverageStatus
  payer_name: str
  member_id: str
  returned_patient: Patient
  copays: CopaySummary
  pharmacy_info: PharmacyInfo
  warnings: list[Warning]


def _format_yyyymmdd(value: str) -> str:
  if len(value) != 8:
      return value

  return f"{value[:4]}-{value[4:6]}-{value[6:]}"


def parse_edi271(raw_271: str) -> Parsed271:
  patient_data = {
      "first_name": "",
      "middle_name": "",
      "last_name": "",
      "date_of_birth": "",
      "address": "",
      "city": "",
      "state": "",
      "postal_code": "",
  }
  payer_name = ""
  member_id = ""
  verification_status = VerificationStatus.pending
  coverage_status = CoverageStatus.unknown
  copays = {
      "primary_care": "",
      "specialist": "",
      "urgent_care": "",
      "pharmacy": "",
  }
  pharmacy_info = {
      "bin": "",
      "pcn": "",
      "group": "",
      "processor": "",
  }
  warnings: list[Warning] = []

  for raw_line in raw_271.splitlines():
      line = raw_line.strip()

      if not line:
          continue

      parts = line.split("*")
      segment = parts[0]

      if segment == "NM1" and len(parts) >= 10 and parts[1] == "PR":
          payer_name = parts[3]
      elif segment == "NM1" and len(parts) >= 10 and parts[1] == "IL":
          patient_data["last_name"] = parts[3]
          patient_data["first_name"] = parts[4]
          member_id = parts[-1]
      elif segment == "DMG" and len(parts) >= 3:
          patient_data["date_of_birth"] = _format_yyyymmdd(parts[2])
      elif segment == "N3" and len(parts) >= 2:
          patient_data["address"] = parts[1]
      elif segment == "N4" and len(parts) >= 4:
          patient_data["city"] = parts[1]
          patient_data["state"] = parts[2]
          patient_data["postal_code"] = parts[3]
      elif segment == "STS" and len(parts) >= 3:
          verification_status = VerificationStatus(parts[1].lower())
          coverage_status = CoverageStatus(parts[2].lower())
      elif segment == "COPAY" and len(parts) >= 3:
          copays[parts[1].lower()] = parts[2]
      elif segment == "RX" and len(parts) >= 3:
          pharmacy_info[parts[1].lower()] = parts[2]
      elif segment == "WARN" and len(parts) >= 4:
          warnings.append(
              Warning(
                  code=parts[1],
                  severity=parts[2].lower(),
                  message="*".join(parts[3:]),
              )
          )

  return Parsed271(
      verification_status=verification_status,
      coverage_status=coverage_status,
      payer_name=payer_name,
      member_id=member_id,
      returned_patient=Patient(**patient_data),
      copays=CopaySummary(**copays),
      pharmacy_info=PharmacyInfo(**pharmacy_info),
      warnings=warnings,
  )
