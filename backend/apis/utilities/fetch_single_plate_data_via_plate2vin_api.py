from .base import models, now, timedelta, logging, PLATE2VIN_API_URL, config, \
        UndefinedValueError, LicensePlateSnapShotsPlate2Vin, \
        clean_string_in_dictionary_object, aiohttp
from .database_sync_to_async import database_sync_to_async
from .fetch_and_save_single_vin_from_nhtsa_api import fetch_and_save_single_vin_from_nhtsa_api

# async function that fetchs a result for a single combo of license plate and state. Vendor: plate2vin

async def fetch_single_plate_data_via_plate2vin_api(license_plate, state, api_url=PLATE2VIN_API_URL):
    logger = logging.getLogger("external_api")
    url = api_url.strip()
    success = False
    payload = {
        "state": state,
        "plate": license_plate
    }
    logger.info('perform async single plate search using plate2vin api...')
    logger.info('attempting to read any api key stored in the .env...')
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
            plate_data = {}
            success = data.get('success')
            if not success:
                return None, success
            elif success:
                vin_data = data.get('vin', {})
                vin = vin_data.get('vin') or None
                vin_data = clean_string_in_dictionary_object(vin_data)
                # saving a record of the vin data associated with this license plate and state to Vin
                if vin:
                    await fetch_and_save_single_vin_from_nhtsa_api(vin)
                    logger.info(
                        f'fetching and saving nhtsa data in progress, for VIN {vin}, which is associated with the license plate {license_plate} and state {state}.')
                else:
                    logger.error('no vin found in the api response....')

                # first need to check if there are any existing records with the same license plate and state. this model deos not check the unique on vin field.
                # exists = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(license_plate=license_plate, state=state).exists)()
                # if exists:
                #     await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(
                #         license_plate=license_plate, state=state
                #     ).update)(version=models.F('version') - 1)
                # update or create a plate_data
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
                        'version': 5,
                    }
                )
            return plate_data, success

