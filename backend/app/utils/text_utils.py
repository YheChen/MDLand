import re


def normalize_whitespace(value: str) -> str:
  return " ".join(value.split()).strip()


def sanitize_filename(value: str) -> str:
  collapsed = normalize_whitespace(value).replace(" ", "_")
  return re.sub(r"[^A-Za-z0-9._-]", "", collapsed) or "upload"
