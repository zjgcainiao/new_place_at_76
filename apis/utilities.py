from datetime import timedelta
from django.utils.timezone import now
from dashboard.async_functions import decrement_version_for_vin_async, update_or_create_vin_snapshots_async, database_sync_to_async
from decouple import config, UndefinedValueError, Csv
from homepageapp.models import LicensePlateSnapShotsPlate2Vin, VinNhtsaApiSnapshots, NhtsaVariableList
from core_operations.common_functions import clean_string_in_dictionary_object
from apis.api_vendor_urls import PLATE2VIN_API_URL, NHTSA_API_URL
from django.db import models
import logging
import aiohttp
import asyncio
from django.core.exceptions import ObjectDoesNotExist
from dashboard.async_functions import database_sync_to_async, fetch_latest_vin_data_from_snapshots
from core_operations.constants import POPULAR_NHTSA_VARIABLE_IDS, POPULAR_NHTSA_GROUP_NAMES
from asgiref.sync import sync_to_async

# API utility function. modified in Dec 2023.


async def fetch_and_save_single_vin_from_nhtsa_api(vin, year=None):
    if year and year.strip():
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json&modelyear={year}"
    else:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json"
    # url_extended = https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}format=json&modelyear={year}
    logger = logging.getLogger('external_api')
    logger.info(
        f'Initiating an api request to NHTSA.DOT.GOV:{ NHTSA_API_URL}.')
    print(f'Initiating an api request to NHTSA.DOT.GOV:{ NHTSA_API_URL}.')
    # print(url)
    vin_data_list = []
    number_of_downgraded_records = 0
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        # if no data, return an warning in the log
        if data is None:
            logger.warning(
                f"No data returned for VIN {vin} and model year {year}. Skipping further processing.")
            print(
                f"No data returned for VIN {vin} and model year {year}. Skipping further processing.")
            return
        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip() or None

        results = data.get("Results")

        if results:
            logger.info(
                f'pulling results for vin {vin} and model year {year} was successful.')
            print(
                f'pulling results for vin {vin} and model year {year} was successful.')

            updated_records = await decrement_version_for_vin_async(vin)
            number_of_downgraded_records = updated_records
            if updated_records:
                logger.info(
                    f'decrementing the version number for existing records with the same vin and variable_id before pulling the latest data...')

            for item in results:
                item = clean_string_in_dictionary_object(item)

                # Check the value of Value
                value = item.get("Value", None)
                # Ensure that value_id is a number, otherwise default to None
                try:
                    value_id = int(item.get("ValueId") or 0)
                    if value_id == 0:
                        value_id = None
                except ValueError:
                    value_id = None

                variable = None  # Default to None if no valid variable is found
                variable_id = item.get("VariableId")

                # Try to convert VariableId to an integer, if it's not None or empty

                if variable_id:
                    try:
                        variable_id = int(variable_id)
                        # Fetch the NhtsaVariableList object corresponding to variable_id
                        variable, created = await database_sync_to_async(NhtsaVariableList.objects.get_or_create)(
                            variable_id=variable_id)
                        # print(
                        #     f'fetching variable instance {variable} and variable_id is {variable_id}')
                    except (ValueError, NhtsaVariableList.DoesNotExist):
                        # If conversion to an integer fails or the variable_id does not exist, leave variable as None
                        pass
                # try:
                #     # Converts None or '' to 0
                #     variable_id = int(item.get("VariableId") or 0)
                #     if variable_id == 0:
                #         variable_id = None
                # except ValueError:
                #     variable_id = None

                # Check the value of Variable_name
                variable_name = item.get("Variable", None)
                if variable_name:
                    variable_name = variable_name.strip() or None

                organized_data = {
                    'results_count': count,
                    'results_message': message,
                    'results_search_criteria': search_criteria,
                    "variable": variable,
                    "variable_name": variable_name,
                    "value": value,
                    "value_id": value_id,
                    "vin": vin,
                    "source": NHTSA_API_URL,
                    "version": 5  # Reset version to 5 for new data
                }

                # updated 2023-11-02 after variable_id becomes a foreign key field
                # variable=variable, override
                vin_data, created = await update_or_create_vin_snapshots_async(vin=vin, variable=variable, data=organized_data)
                print(f'vin_data is {vin_data}')
                vin_data_list.append(vin_data)

        logger.info(
            f'Vin data has been saved for {vin} and model year {year}. created?:{created}.')

        if created:
            print(f'saving new vin data? : {created}.')
        else:
            print('no new vin data saved...')

        print('function is completed.')
        # return the data, the number of records downgraded, and if new records are created in the VinNhtsaSnapshots
        return vin_data_list, number_of_downgraded_records, created

    except (aiohttp.ClientError, aiohttp.ClientPayloadError) as e:
        logger.error(
            f"Failed to fetch VIN data for {vin} and model year {year}. Error: {e}")
        return None, None, None
    except Exception as e:
        logger.error(
            f"Failed to process and save VIN data for {vin} and model year {year}. Error: {e}")
        return None, None, None

# async function that fetchs a result for a single combo of license plate and state. Vendor: plate2vin


async def fetch_single_plate_data_via_plate2vin_api(license_plate, state, api_url=PLATE2VIN_API_URL):
    logger = logging.getLogger('external_api')
    url = api_url.strip()
    payload = {
        "state": state,
        "plate": license_plate
    }
    logger.info('perform async single plate search using plate2vin api...')
    logger.info('attempting to read any api key stored in the .env...')
    try:
        plate2vin_api_key = config("PLATE2VIN_API_KEY")
    except UndefinedValueError:
        logger.error(
            'Error: The required environment variable PLATE2VIN_API_KEY is not set.')
        raise ValueError(
            "The required environment variable PLATE2VIN_API_KEY is not set.")

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
        return await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(
            license_plate=license_plate,
            state=state,
            last_checked_at__gte=twelve_months_ago
        ).order_by('-last_checked_at').first)()

    # start the api call.
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()

            success = data.get('success')
            if not success:
                return None, success
            elif success:
                vin_data = data.get('vin', {})
                vin_data = clean_string_in_dictionary_object(vin_data)

                if vin_data.get('vin'):
                    new_vin = vin_data.get('vin')
                    await fetch_and_save_single_vin_from_nhtsa_api(new_vin)
                    logger.info(
                        f'fetching nhtsa data for the vin {new_vin} associated with the lience plate {license_plate}')
                # first need to check if there are any existing records with the same license plate and state. this model deos not check the unique on vin field.
                exists = await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(license_plate=license_plate, state=state).exists)()
                if exists:
                    await database_sync_to_async(LicensePlateSnapShotsPlate2Vin.objects.filter(
                        license_plate=license_plate, state=state
                    ).update)(version=models.F('version') - 1)
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


# Define a synchronous function to get the QuerySet of VinNhtsaApiSnapshots (vin_data).
# the function is created to be used in async fetch_latest_vin_data_func()
def get_vin_snapshot_queryset(vin, variable_ids_list=POPULAR_NHTSA_VARIABLE_IDS, group_names_list=POPULAR_NHTSA_GROUP_NAMES):
    return VinNhtsaApiSnapshots.objects.filter(
        vin=vin,
        version=5,
        variable__variable_id__in=variable_ids_list,
        variable__variable_group_name__in=group_names_list,
    ).select_related('variable').order_by('-created_at', 'vin', 'variable')


async def fetch_latest_vin_data_func(vin, variable_ids_list=POPULAR_NHTSA_VARIABLE_IDS, group_names_list=POPULAR_NHTSA_GROUP_NAMES):

    logger = logging.getLogger('external_api')

    # List of variable IDs to filter
    variable_ids_list = POPULAR_NHTSA_VARIABLE_IDS

    print('initiating async function `fetch_latest_vin_data_func` to fetch vin info. pouplar fields only. ')

    # Convert the synchronous exists() call to an async call using sync_to_async and await it
    vin_exists = await sync_to_async(VinNhtsaApiSnapshots.objects.filter(vin=vin).exists, thread_sensitive=True)()
    logger.info(f'checking if vin {vin} records exist in database...')
    print(f'checking if vin {vin} records exist in database...')
    if not vin_exists:
        # VIN does not exist, so fetch and save the VIN data
        # Ensure the fetch_and_save_single_vin_from_nhtsa_api is an async function or properly awaited if using sync_to_async
        await fetch_and_save_single_vin_from_nhtsa_api(vin)

    # Includes a join on the related NhtsaVariableList table and filter on the variable_group_name
    # Now retrieve the filtered records asynchronously
    queryset = await sync_to_async(
        get_vin_snapshot_queryset, thread_sensitive=True)(vin)

    return queryset
