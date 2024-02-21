# API utility function. modified in Dec 2023.
from .base import models, now, timedelta, logging, NHTSA_API_URL, config, \
        UndefinedValueError, VinNhtsaApiSnapshots, \
        clean_string_in_dictionary_object, aiohttp, NhtsaVariableList, \
        logger

from .database_sync_to_async import database_sync_to_async
from .decrement_version_for_vin_async import decrement_version_for_vin_async
from .update_or_create_vin_snapshots_async import update_or_create_vin_snapshots_async

async def fetch_and_save_single_vin_from_nhtsa_api(vin, year=None):
    if year and year.strip():
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json&modelyear={year}"
    else:
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json"
    # url_extended = https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}format=json&modelyear={year}
    logger.info(
        f'Initiating an api request to { NHTSA_API_URL}.')
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
            return
        # Process and save the data as you do in your management script.
        # Fetch the `count`, `message`, `SearchCriteria`, `Results` from the api result.
        count = data.get("Count", None)
        message = data.get("Message", "").strip() or None
        search_criteria = data.get("SearchCriteria", "").strip() or None

        results = data.get("Results")

        if results:
            logger.info(
                f"result fetched successful for vin {vin} and model year {year}.")

            # updated_records = await decrement_version_for_vin_async(vin)
            # number_of_downgraded_records = updated_records
            # if updated_records:
            #     logger.info(
            #         f'decrementing the version number for existing records with the same vin and variable_id before pulling the latest data...')

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
                    # "version": 5  # this field is not needed here
                }

                # updated 2023-11-02 after variable_id becomes a foreign key field
                # variable=variable, override
                # vin_data, created = await update_or_create_vin_snapshots_async(vin=vin, variable=variable, data=organized_data)
                
                # updated on 2023-12-24: async function, to create or update in VinNhtsaApiSnapshots model.
                vin_data,created = await database_sync_to_async(VinNhtsaApiSnapshots.objects.update_or_create)(
                        vin=vin,
                        variable=variable,
                        defaults=organized_data,
                    )
                logger.info(f'vin_data is {vin_data}')
                vin_data_list.append(vin_data)

        logger.info(
            f'Vin data has been saved for {vin} and model year {year}. new vin data created?:{created}.')

        if created:
            logger.info(f'saving new vin snapshots? : {created}.')
        else:
            logger.info(' updating existing vin snapshots...')
        logger.info('function is completed.')
        # print('function is completed.')
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
