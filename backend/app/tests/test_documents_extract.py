def test_documents_extract_returns_structured_data(client, sample_png_bytes):
  files = {
      "driver_license": ("drivers-license.png", sample_png_bytes, "image/png"),
      "insurance_front": ("insurance-front.png", sample_png_bytes, "image/png"),
      "insurance_back": ("insurance-back.png", sample_png_bytes, "image/png"),
  }

  response = client.post("/api/documents/extract", files=files)

  assert response.status_code == 200

  payload = response.json()

  assert payload["patient"]["firstName"] == "Avery"
  assert payload["insurance"]["memberId"] == "XJH123456789"
  assert payload["confidence"] == 0.93
  assert len(payload["documentNotes"]) == 3
  assert len(payload["warnings"]) == 2
