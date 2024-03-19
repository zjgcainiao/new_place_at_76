from .base import models, now, timedelta, logging, PLATE2VIN_API_URL, config, \
    UndefinedValueError, LicensePlateSnapShotsPlate2Vin, \
    clean_string_in_dictionary_object, aiohttp, sync_to_async
from .database_sync_to_async import database_sync_to_async
from .fetch_and_save_single_vin_from_nhtsa_api import fetch_and_save_single_vin_from_nhtsa_api
import json
# async function that fetchs a result for a single combo of license plate and state. Vendor: plate2vin


async def fetch_single_plate_data_via_plate2vin_api(license_plate, state, api_url=PLATE2VIN_API_URL):
    logger = logging.getLogger("external_api")
    url = api_url.strip()
    success = False
    payload = {
        "state": state,
        "plate": license_plate
    }
    logger.info('running fetch_single_plate_data_via_plate2vin_api...')
    try:
        plate2vin_api_key = config("PLATE2VIN_API_KEY")
        logger.info("the api key found ...")
    except UndefinedValueError:
        logger.error(
            "Error: The required environment variable`PLATE2VIN_API_KEY` is not set.")
        raise ValueError(
            "The required environment variable `PLATE2VIN_API_KEY` is not set.")

    headers = {
        'Authorization': plate2vin_api_key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # check if a record exists already in the database first before initiating a api call:
    # first need to check if there are any existing records with the same license plate and state.
    # this model does not check the unique on vin field.

    # Calculate the date for 12 months ago from today
    twelve_months_ago = now() - timedelta(days=365)

    # Modify the query to check if last_checked_at is within the last 12 months
    exists = await database_sync_to_async(
        LicensePlateSnapShotsPlate2Vin.objects.filter(
            license_plate=license_plate,
            state=state,
            last_checked_at__gte=twelve_months_ago
        ).exists
    )()
    # exists = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(license_plate=license_plate, state=state).exists)()
    if exists:
        success = True
        return await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(
            license_plate=license_plate,
            state=state,
            last_checked_at__gte=twelve_months_ago
        ).order_by('-last_checked_at').first)(), success

    # start the api call.
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()
    if not data:
        success = False
        logger.error(
            f"Failed to fetch plate data for {license_plate} and state {state}.")
        return None, success

    plate_data = {}
    success = data.get('success')

    vin_data = data.get('vin', {})
    vin = vin_data.get('vin') or None
    # vin_data = clean_string_in_dictionary_object(vin_data)
    # Ensure vin_data is a dictionary
    if isinstance(vin_data, str):
        try:
            vin_data = json.loads(vin_data)
            logger.info(
                f'vin_data converted from string to dictionary: {vin_data}')
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding vin_data string: {e}')
            vin_data = {}  # Default to an empty dictionary in case of error
        logger.info(f'vin_data fetched from Plate2Vin API: {vin_data}...')
    # saving a record of the vin data associated with this license plate and state to Vin
    if vin:
        logger.info(
            f'VIN {vin} found in the license plate search response....fetching additional vin info from nhtsa api...')
        vin_snapshot_list, search_criteria, message = await fetch_and_save_single_vin_from_nhtsa_api(vin)
        logger.info(
            f'VIN {vin} is associated with license plate {license_plate} && state {state}....')
    else:
        logger.error('no vin found in the api response....')

    plate_data, created = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.update_or_create)(
        license_plate=license_plate,
        state=state,
        defaults={
            'vin': vin_data.get('vin'),
            'api_url': api_url,
            'api_response': data,
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
        }
    )
    logger.info(f'plate_data: {plate_data}...created: {created}...')
    return plate_data, success
