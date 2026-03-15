from imghdr import what as detect_image_type

from fastapi import HTTPException, UploadFile, status

from app.constants import (
    ALLOWED_IMAGE_CONTENT_TYPES,
    ALLOWED_IMAGE_FORMATS,
    MAX_UPLOAD_SIZE_BYTES,
)


async def validate_image_upload(upload: UploadFile, label: str) -> bytes:
  filename = upload.filename or label
  file_bytes = await upload.read()

  if not file_bytes:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"{label} is empty. Please upload a valid image file.",
      )

  if len(file_bytes) > MAX_UPLOAD_SIZE_BYTES:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"{label} exceeds the {MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)} MB limit.",
      )

  if upload.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"{label} must be a JPG, PNG, or WEBP image.",
      )

  detected_format = detect_image_type(None, file_bytes)

  if detected_format not in ALLOWED_IMAGE_FORMATS:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"{filename} could not be recognized as a readable image.",
      )

  return file_bytes
