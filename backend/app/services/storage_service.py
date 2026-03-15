from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from app.config import get_settings
from app.utils.text_utils import sanitize_filename


@dataclass
class StoredDocument:
  document_type: str
  original_filename: str
  stored_filename: str
  content_type: str
  file_path: str


def save_upload(
    document_type: str,
    original_filename: str,
    content_type: str,
    file_bytes: bytes,
) -> StoredDocument:
  settings = get_settings()
  upload_root = Path(settings.upload_dir)
  document_dir = upload_root / document_type
  document_dir.mkdir(parents=True, exist_ok=True)

  sanitized_name = sanitize_filename(original_filename)
  stored_filename = f"{uuid4().hex}_{sanitized_name}"
  destination = document_dir / stored_filename
  destination.write_bytes(file_bytes)

  return StoredDocument(
      document_type=document_type,
      original_filename=original_filename,
      stored_filename=stored_filename,
      content_type=content_type,
      file_path=str(destination.resolve()),
  )
