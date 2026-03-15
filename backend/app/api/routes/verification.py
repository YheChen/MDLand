from fastapi import APIRouter

from app.schemas.verification import VerificationRequest, VerificationResponse
from app.services.verification_service import verify_eligibility

router = APIRouter()


@router.post("/verify", response_model=VerificationResponse)
def verify_eligibility_route(payload: VerificationRequest) -> VerificationResponse:
  return verify_eligibility(payload)
