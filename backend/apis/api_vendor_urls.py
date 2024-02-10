
vin = None
year = None
make = None
model = None

# https://www.nhtsa.gov/nhtsa-datasets-and-apis
NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api"
NHTSA_API_HOMEPAGE = "https://vpic.nhtsa.dot.gov/api"
NHTSA_API_DECODED_VIN_EXTENDED = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json&modelyear={year}"
NHTSA_API_RECALLS = f"api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"
PLATE2VIN_API_URL = 'https://platetovin.com/api/convert'

PLATE2VIN_API_RATE_LIMIT = 10
