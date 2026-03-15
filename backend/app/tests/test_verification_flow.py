def test_verification_flow_returns_summary_and_raw_271(client):
  payload = {
      "patient": {
          "firstName": "Avery",
          "middleName": "Jordan",
          "lastName": "Carter",
          "dateOfBirth": "1988-11-04",
          "address": "123 Harbor Street",
          "city": "Baltimore",
          "state": "MD",
          "postalCode": "21201",
      },
      "insurance": {
          "payerName": "Blue Cross Blue Shield of Maryland",
          "payerId": "BCBSMD01",
          "memberId": "XJH123456789",
          "groupNumber": "GRP-45029",
          "rxBin": "610279",
          "rxPcn": "03200000",
          "rxGroup": "MDRX01",
      },
  }

  response = client.post("/api/verification/verify", json=payload)

  assert response.status_code == 200

  body = response.json()

  assert body["summary"]["verificationStatus"] == "verified"
  assert body["summary"]["coverageStatus"] == "active"
  assert body["summary"]["payerName"] == "Blue Cross Blue Shield of Maryland"
  assert body["summary"]["memberId"] == "XJH123456789"
  assert body["summary"]["discrepancies"][0]["field"] == "address"
  assert "ISA*00*" in body["raw271"]
  assert body["warnings"][0]["code"] == "COPAY-DUE"
