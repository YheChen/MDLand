from app.services import extraction_service
from app.services.extraction_service import OCRDocumentResult


def test_documents_extract_returns_structured_data(client, sample_png_bytes, monkeypatch):
  def fake_run_ocr_for_documents(_documents):
      return [
          OCRDocumentResult(
              document_type="driver_license",
              text="",
              lines=[
                  "CARTER",
                  "AVERY JORDAN",
                  "EXP 11/04/2028",
                  "ISS 11/04/2020",
                  "11/04/1988",
                  "123 Harbor Street",
                  "Baltimore MD 21201",
              ],
              confidence=89.0,
              variant="grayscale",
          ),
          OCRDocumentResult(
              document_type="insurance_id",
              text="",
              lines=[
                  "() UnitedHealthcare",
                  "MEMBER ID XJH123456789 GROUP NUMBER GRP-45029",
                  "PAYER ID 87726",
                  "RX BIN 610279",
                  "RX PCN 9999",
                  "RX GROUP NUMBER98765",
              ],
              confidence=86.0,
              variant="grayscale",
          ),
      ]

  monkeypatch.setattr(
      "app.services.extraction_service.run_ocr_for_documents",
      fake_run_ocr_for_documents,
  )

  files = {
      "driver_license": ("drivers-license.png", sample_png_bytes, "image/png"),
      "insurance_id": ("insurance-id.png", sample_png_bytes, "image/png"),
  }

  response = client.post("/api/documents/extract", files=files)

  assert response.status_code == 200

  payload = response.json()

  assert payload["patient"]["firstName"] == "Avery"
  assert payload["patient"]["middleName"] == "Jordan"
  assert payload["patient"]["lastName"] == "Carter"
  assert payload["patient"]["dateOfBirth"] == "1988-11-04"
  assert payload["insurance"]["payerName"] == "UnitedHealthcare"
  assert payload["insurance"]["payerId"] == "87726"
  assert payload["insurance"]["memberId"] == "XJH123456789"
  assert payload["insurance"]["groupNumber"] == "GRP-45029"
  assert payload["insurance"]["rxBin"] == "610279"
  assert payload["insurance"]["rxPcn"] == "9999"
  assert payload["insurance"]["rxGroup"] == "98765"
  assert payload["confidence"] > 0.8
  assert len(payload["documentNotes"]) == 2
  assert payload["missingFields"] == []
  assert payload["warnings"][0]["code"] == "OCR-REVIEW"


def test_documents_extract_reports_missing_fields(client, sample_png_bytes, monkeypatch):
  def fake_run_ocr_for_documents(_documents):
      return [
          OCRDocumentResult(
              document_type="driver_license",
              text="",
              lines=[
                  "FIRST NAME",
                  "Avery",
                  "LAST NAME",
                  "Carter",
              ],
              confidence=42.0,
              variant="grayscale",
          ),
          OCRDocumentResult(
              document_type="insurance_id",
              text="",
              lines=[],
              confidence=0.0,
              variant="grayscale",
          ),
      ]

  monkeypatch.setattr(
      "app.services.extraction_service.run_ocr_for_documents",
      fake_run_ocr_for_documents,
  )

  files = {
      "driver_license": ("drivers-license.png", sample_png_bytes, "image/png"),
      "insurance_id": ("insurance-id.png", sample_png_bytes, "image/png"),
  }

  response = client.post("/api/documents/extract", files=files)

  assert response.status_code == 200

  payload = response.json()

  assert "dateOfBirth" in payload["missingFields"]
  assert "payerName" in payload["missingFields"]
  assert "memberId" in payload["missingFields"]
  assert "rxBin" in payload["missingFields"]
  warning_codes = {warning["code"] for warning in payload["warnings"]}
  assert "OCR-NO-TEXT" in warning_codes
  assert "OCR-LOW-CONFIDENCE" in warning_codes
  assert "EXTRACTION-INCOMPLETE" in warning_codes


def test_documents_extract_rejects_implausible_driver_license_fields(
    client,
    sample_png_bytes,
    monkeypatch,
):
  def fake_run_ocr_for_documents(_documents):
      return [
          OCRDocumentResult(
              document_type="driver_license",
              text="",
              lines=[
                  "NEW YORK",
                  "S",
                  "10/31/1990",
                  "REET",
                  "Albany NY 12222",
              ],
              confidence=71.0,
              variant="upscaled:psm11",
          ),
          OCRDocumentResult(
              document_type="insurance_id",
              text="",
              lines=[
                  "i) UnitedHealthcare",
                  "MEMBER ID 123456789",
                  "PAYER ID 87726",
                  "GROUP NUMBER 98765",
                  "RX BIN 610279",
                  "RX PCN 9999",
                  "RX GROUP UHEALTH",
              ],
              confidence=89.0,
              variant="grayscale:psm6",
          ),
      ]

  monkeypatch.setattr(
      "app.services.extraction_service.run_ocr_for_documents",
      fake_run_ocr_for_documents,
  )

  files = {
      "driver_license": ("drivers-license.png", sample_png_bytes, "image/png"),
      "insurance_id": ("insurance-id.png", sample_png_bytes, "image/png"),
  }

  response = client.post("/api/documents/extract", files=files)

  assert response.status_code == 200

  payload = response.json()

  assert payload["patient"]["firstName"] == ""
  assert payload["patient"]["middleName"] == ""
  assert payload["patient"]["lastName"] == ""
  assert payload["patient"]["dateOfBirth"] == "1990-10-31"
  assert payload["patient"]["address"] == ""
  assert payload["insurance"]["payerName"] == "UnitedHealthcare"
  assert "firstName" in payload["missingFields"]
  assert "lastName" in payload["missingFields"]
  assert "address" in payload["missingFields"]
  warning_codes = {warning["code"] for warning in payload["warnings"]}
  assert "EXTRACTION-PLAUSIBILITY" in warning_codes
  assert "EXTRACTION-INCOMPLETE" in warning_codes


def test_driver_license_parser_ignores_unlabeled_one_letter_middle_initial():
  result = OCRDocumentResult(
      document_type="driver_license",
      text="",
      lines=[
          "MICHELLE",
          "MARIE T",
          "10/31/1990",
          "123 Harbor Street",
          "Albany NY 12222",
      ],
      confidence=77.0,
      variant="identity_upscaled:psm11",
  )

  fields = extraction_service._extract_driver_license_fields(result)

  assert fields["first_name"] == "MARIE"
  assert fields["middle_name"] == ""
  assert fields["last_name"] == "MICHELLE"
  assert fields["state"] == "NY"


def test_driver_license_parser_prefers_full_state_name_over_bad_abbreviation():
  result = OCRDocumentResult(
      document_type="driver_license",
      text="",
      lines=[
          "NEW YORK",
          "MICHELLE",
          "MARIE T",
          "123 Harbor Street",
          "Albany KY 12222",
      ],
      confidence=73.0,
      variant="composite[identity_upscaled:psm11, address_upscaled:psm6]",
  )

  fields = extraction_service._extract_driver_license_fields(result)

  assert fields["state"] == "NY"
  assert fields["city"] == "Albany"
  assert fields["postal_code"] == "12222"
