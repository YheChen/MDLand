from app.schemas.common import APIModel


class ErrorResponse(APIModel):
  detail: str
