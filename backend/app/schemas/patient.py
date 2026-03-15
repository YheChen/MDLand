from app.schemas.common import APIModel


class Patient(APIModel):
  first_name: str
  middle_name: str = ""
  last_name: str
  date_of_birth: str
  address: str
  city: str
  state: str
  postal_code: str
