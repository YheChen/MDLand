from app.schemas.insurance import Insurance
from app.schemas.patient import Patient
from app.schemas.verification import VerificationRequest
from app.services.edi271_generator import generate_edi271
from app.services.edi271_parser import parse_edi271
from app.services.rule_engine import evaluate_eligibility


def test_edi271_parser_extracts_core_fields():
  request = VerificationRequest(
      patient=Patient(
          first_name="Avery",
          middle_name="Jordan",
          last_name="Carter",
          date_of_birth="1988-11-04",
          address="123 Harbor Street",
          city="Baltimore",
          state="MD",
          postal_code="21201",
      ),
      insurance=Insurance(
          payer_name="Blue Cross Blue Shield of Maryland",
          payer_id="BCBSMD01",
          member_id="XJH123456789",
          group_number="GRP-45029",
          rx_bin="610279",
          rx_pcn="03200000",
          rx_group="MDRX01",
      ),
  )

  raw_271 = generate_edi271(request, evaluate_eligibility(request))
  parsed = parse_edi271(raw_271)

  assert parsed.verification_status.value == "verified"
  assert parsed.coverage_status.value == "active"
  assert parsed.payer_name == "Blue Cross Blue Shield of Maryland"
  assert parsed.member_id == "XJH123456789"
  assert parsed.pharmacy_info.bin == "610279"
  assert parsed.returned_patient.address.endswith("Apt 2")
