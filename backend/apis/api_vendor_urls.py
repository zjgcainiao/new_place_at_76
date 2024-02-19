
PLATE2VIN_API_URL = 'https://platetovin.com/api/convert'
PLATE2VIN_API_RATE_LIMIT = 10

# https://www.nhtsa.gov/nhtsa-datasets-and-apis

NHTSA_API_URL = "https://vpic.nhtsa.dot.gov/api"
NHTSA_API_HOMEPAGE = "https://vpic.nhtsa.dot.gov/api"


def nhtsa_get_decoded_vin_extended_flat_format_url(vin, year=None):
    return f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinvaluesextended/{vin}?format=json" + (f"&modelyear={year}" if year else "")

def nhtsa_get_all_makes_url():
    return f"https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json"


def nhtsa_get_safety_rating_by_vehicle_id_url(vehicle_id):
    return f"https://api.nhtsa.gov/SafetyRatings/VehicleId/{vehicle_id}"

def nhtsa_get_vehicle_id_url(make, model, year):
    return f"https://api.nhtsa.gov/SafetyRatings/modelyear/{year}/make/{make}/model/{model}"

def nhtsa_get_complaints_by_vehicle_id_url(make,model,year):
    return f"https://api.nhtsa.gov/complaints/complaintsByVehicle?make={make}&model={model}&modelYear={year}"

def nhtsa_get_recalls_url(make,model,year):
    return f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={make}&model={model}&modelYear={year}"

def nhtsa_get_decoded_vin_extended_url(vin, year=None):
    return f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json" + (f"&modelyear={year}" if year else "")



def nhtsa_get_models_for_make_id_url(make):
    return f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/{make}?format=json"

def construct_car_seat_inspector_location_url(base_url, pattern_type, **kwargs):
    """
    Construct a URL based on the provided base URL and pattern type.
    
    Args:
        base_url (str): The base URL.
        pattern_type (str): The type of URL pattern.
        **kwargs: Keyword arguments representing dynamic parts of the URL.
                  For example, for the pattern /CSSIStation/zip/63640, kwargs
                  would be {'zip_code': '63640'}.

    Returns:
        str: The constructed URL.

    Raises:
        ValueError: If an incorrect pattern type is provided.
    """
    if pattern_type == 'zip':
        if 'zip_code' in kwargs:
            return f"{base_url}/CSSIStation/zip/{kwargs['zip_code']}"
        else:
            raise ValueError("Missing zip_code argument for pattern type 'zip'")
    elif pattern_type == 'state':
        if 'state_code' in kwargs:
            return f"{base_url}/api/CSSIStation/state/{kwargs['state_code']}"
        else:
            raise ValueError("Missing state_code argument for pattern type 'state'")
    elif pattern_type == 'latlong':
        if all(key in kwargs for key in ['lat', 'long', 'miles']):
            return f"{base_url}/CSSIStation?lat={kwargs['lat']}&long={kwargs['long']}&miles={kwargs['miles']}"
        else:
            raise ValueError("Missing one or more of the required arguments (lat, long, miles) for pattern type 'latlong'")
    else:
        raise ValueError("Invalid pattern type")