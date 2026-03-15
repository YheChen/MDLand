from app.schemas.summary import VerificationSummary
from app.schemas.verification import VerificationRequest, VerificationResponse
from app.services.discrepancy_service import detect_discrepancies
from app.services.edi271_generator import generate_edi271
from app.services.edi271_parser import parse_edi271
from app.services.rule_engine import evaluate_eligibility
from app.utils.date_utils import utc_now


def verify_eligibility(request: VerificationRequest) -> VerificationResponse:
  rule_result = evaluate_eligibility(request)
  raw_271 = generate_edi271(request, rule_result)
  parsed_271 = parse_edi271(raw_271)
  discrepancies = detect_discrepancies(request, parsed_271)

  summary = VerificationSummary(
      verification_status=parsed_271.verification_status,
      coverage_status=parsed_271.coverage_status,
      payer_name=parsed_271.payer_name or request.insurance.payer_name,
      member_id=parsed_271.member_id or request.insurance.member_id,
      copays=parsed_271.copays,
      pharmacy_info=parsed_271.pharmacy_info,
      discrepancies=discrepancies,
  )

  return VerificationResponse(
      summary=summary,
      warnings=parsed_271.warnings or rule_result.warnings,
      raw_271=raw_271,
      checked_at=utc_now(),
  )
