from .database_sync_to_async import database_sync_to_async
from homepageapp.models import LicensePlateSnapShotsPlate2Vin

@database_sync_to_async
def fetch_latest_plate_data_from_snapshots(plate, state_abbr):
    return LicensePlateSnapShotsPlate2Vin.objects.filter(
        license_plate=plate,
        state=state_abbr,
    )
