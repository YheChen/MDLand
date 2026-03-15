from app.schemas.verification import VerificationRequest
from app.services.rule_engine import RuleEngineResult


def generate_edi271(
    request: VerificationRequest,
    result: RuleEngineResult,
) -> str:
  patient = result.returned_patient
  insurance = request.insurance

  lines = [
      "ISA*00*          *00*          *ZZ*MDLAND         *ZZ*ELIGIBILITY    *260314*1200*^*00501*000000905*0*T*:",
      "GS*HB*MDLAND*ELIGIBILITY*20260314*1200*1*X*005010X279A1",
      "ST*271*0001*005010X279A1",
      "BHT*0022*11*10001234*20260314*1200",
      f"NM1*PR*2*{insurance.payer_name}*****PI*{insurance.payer_id}",
      f"NM1*IL*1*{patient.last_name}*{patient.first_name}****MI*{insurance.member_id}",
      f"DMG*D8*{patient.date_of_birth.replace('-', '')}",
      f"N3*{patient.address}",
      f"N4*{patient.city}*{patient.state}*{patient.postal_code}",
      f"STS*{result.verification_status.value.upper()}*{result.coverage_status.value.upper()}",
      f"COPAY*PRIMARY_CARE*{result.copays.primary_care}",
      f"COPAY*SPECIALIST*{result.copays.specialist}",
      f"COPAY*URGENT_CARE*{result.copays.urgent_care}",
      f"COPAY*PHARMACY*{result.copays.pharmacy}",
      f"RX*BIN*{result.pharmacy_info.bin}",
      f"RX*PCN*{result.pharmacy_info.pcn}",
      f"RX*GROUP*{result.pharmacy_info.group}",
      f"RX*PROCESSOR*{result.pharmacy_info.processor}",
  ]

  for warning in result.warnings:
      lines.append(
          f"WARN*{warning.code}*{warning.severity.value.upper()}*{warning.message}"
      )

  lines.extend(
      [
          "SE*18*0001",
          "GE*1*1",
          "IEA*1*000000905",
      ]
  )

  return "\n".join(lines)
