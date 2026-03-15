from enum import Enum

from pydantic import BaseModel, ConfigDict


def to_camel(value: str) -> str:
  parts = value.split("_")
  return parts[0] + "".join(part.capitalize() for part in parts[1:])


class APIModel(BaseModel):
  model_config = ConfigDict(
      alias_generator=to_camel,
      populate_by_name=True,
      from_attributes=True,
  )


class WarningSeverity(str, Enum):
  info = "info"
  warning = "warning"
  critical = "critical"


class VerificationStatus(str, Enum):
  verified = "verified"
  pending = "pending"
  manual_review = "manual_review"


class CoverageStatus(str, Enum):
  active = "active"
  inactive = "inactive"
  unknown = "unknown"


class Warning(APIModel):
  code: str
  message: str
  severity: WarningSeverity


class HealthResponse(APIModel):
  status: str
