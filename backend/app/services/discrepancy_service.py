from app.schemas.summary import Discrepancy
from app.schemas.verification import VerificationRequest
from app.services.edi271_parser import Parsed271


def detect_discrepancies(
    request: VerificationRequest,
    parsed_271: Parsed271,
) -> list[Discrepancy]:
  comparisons = [
      (
          "address",
          request.patient.address,
          parsed_271.returned_patient.address,
          "Eligibility source returned a different service address.",
      ),
      (
          "city",
          request.patient.city,
          parsed_271.returned_patient.city,
          "Eligibility source returned a different city value.",
      ),
      (
          "state",
          request.patient.state,
          parsed_271.returned_patient.state,
          "Eligibility source returned a different state value.",
      ),
      (
          "postalCode",
          request.patient.postal_code,
          parsed_271.returned_patient.postal_code,
          "Eligibility source returned a different postal code.",
      ),
      (
          "payerName",
          request.insurance.payer_name,
          parsed_271.payer_name,
          "Eligibility source returned a different payer name.",
      ),
      (
          "memberId",
          request.insurance.member_id,
          parsed_271.member_id,
          "Eligibility source returned a different member ID.",
      ),
  ]

  discrepancies: list[Discrepancy] = []

  for field, extracted_value, verified_value, note in comparisons:
      if extracted_value.strip() and verified_value.strip() and extracted_value != verified_value:
          discrepancies.append(
              Discrepancy(
                  field=field,
                  extracted_value=extracted_value,
                  verified_value=verified_value,
                  note=note,
              )
          )

  return discrepancies
