
from asgiref.sync import sync_to_async
from homepageapp.models import VinNhtsaAPISnapshots
from django.db import models
import asyncio
from django.db import close_old_connections
import json
from homepageapp.models import LicensePlateSnapShotsPlate2Vin
import aiohttp
from apis.api_vendor_urls import PLATE2VIN_API_URL
from core_operations.common_functions import clean_string_in_dictionary_object


# this is a custom version of sync_to_async function that explcitly control database connections
# 1. manages the connection's lifecycle expliclty, ensure that connections are properly closed afer usage.
# 2. i can add logiging speicifc to database operations.
# 3. can cutomize common database exceptions uniformly.

def database_sync_to_async(func):
    """
    Turn a sync function that interacts with the database into an async function.
    Handles database connection management and common exception handling.
    """

    @sync_to_async
    def wrapper(*args, **kwargs):
        try:
            # Ensure old DB connections are closed
            close_old_connections()
            # Execute the function
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Handle common database exceptions if required.
            # For example: handle DatabaseError, IntegrityError, etc.
            # You can log the exception or take other corrective actions.
            raise e
        finally:
            # Ensure old DB connections are closed after function execution
            close_old_connections()

    return wrapper


@database_sync_to_async
def decrement_version_for_vin_async(vin):

    return VinNhtsaAPISnapshots.objects.filter(vin=vin).update(
        version=models.F('version') - 1
    )


@database_sync_to_async
def update_or_create_vin_snapshots_async(vin, variable_id, data):
    return VinNhtsaAPISnapshots.objects.update_or_create(
        vin=vin,
        variable_id=variable_id,
        defaults=data,
    )

# async function that fetchs a result for a single combo of license plate and state


async def fetch_single_plate_data_via_plate2vin_async(license_plate, state, headers, api_url=PLATE2VIN_API_URL):
    url = api_url.strip()
    payload = {
        "state": state,
        "plate": license_plate
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()

            success = data.get('success')
            vin_data = data.get('vin', {})
            if success:
                vin_data = clean_string_in_dictionary_object(vin_data)
                # first need to check if the existing system
                exists = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(license_plate=license_plate, state=state).exists)()
                if exists:
                    await sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(
                        license_plate=license_plate, state=state
                    ).update, thread_sensitive=True)(version=models.F('version') - 1)
                # update or create
                await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.update_or_create)(
                    license_plate=license_plate,
                    state=state,
                    defaults={
                        'vin': vin_data.get('vin'),
                        'api_url': api_url,
                        'api_response': json.dumps(data),
                        'year': vin_data.get('year'),
                        'make': vin_data.get('make'),
                        'model': vin_data.get('model'),
                        'trim': vin_data.get('trim'),
                        'name': vin_data.get('name'),
                        'engine': vin_data.get('engine'),
                        'style': vin_data.get('style'),
                        'transmission': vin_data.get('transmission'),
                        'drive_type': vin_data.get('driveType'),
                        'fuel': vin_data.get('fuel'),
                        'color_name': vin_data.get('color', {}).get('name'),
                        'color_abbreviation': vin_data.get('color', {}).get('abbreviation'),
                        'version': 5,
                    }
                )
            return vin_data, success
