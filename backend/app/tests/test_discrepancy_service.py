from app.schemas.common import CoverageStatus, VerificationStatus
from app.schemas.insurance import Insurance
from app.schemas.patient import Patient
from app.schemas.summary import CopaySummary, PharmacyInfo
from app.schemas.verification import VerificationRequest
from app.services.discrepancy_service import detect_discrepancies
from app.services.edi271_parser import Parsed271


def test_discrepancy_service_detects_address_difference():
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
  parsed_271 = Parsed271(
      verification_status=VerificationStatus.verified,
      coverage_status=CoverageStatus.active,
      payer_name="Blue Cross Blue Shield of Maryland",
      member_id="XJH123456789",
      returned_patient=Patient(
          first_name="Avery",
          middle_name="Jordan",
          last_name="Carter",
          date_of_birth="1988-11-04",
          address="123 Harbor Street, Apt 2",
          city="Baltimore",
          state="MD",
          postal_code="21201",
      ),
      copays=CopaySummary(
          primary_care="$25",
          specialist="$40",
          urgent_care="$60",
          pharmacy="Tiered copay plan",
      ),
      pharmacy_info=PharmacyInfo(
          bin="610279",
          pcn="03200000",
          group="MDRX01",
          processor="MedRx Advance",
      ),
      warnings=[],
  )

  discrepancies = detect_discrepancies(request, parsed_271)

  assert len(discrepancies) == 1
  assert discrepancies[0].field == "address"
